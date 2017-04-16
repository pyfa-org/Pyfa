import base64
from logbook import Logger
import os
import re
import time
import zlib

import requests
from requests.adapters import HTTPAdapter

import config
from service.pycrest.compat import bytes_, text_
from service.pycrest.errors import APIException

from urlparse import urlparse, urlunparse, parse_qsl

try:
    import pickle
except ImportError:  # pragma: no cover
    # noinspection PyPep8Naming
    import cPickle as pickle

pyfalog = Logger(__name__)
cache_re = re.compile(r'max-age=([0-9]+)')


class APICache(object):
    def put(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def invalidate(self, key):
        raise NotImplementedError


class FileCache(APICache):
    def __init__(self, path):
        self._cache = {}
        self.path = path
        if not os.path.isdir(self.path):
            os.mkdir(self.path, 0o700)

    def _getpath(self, key):
        return os.path.join(self.path, str(hash(key)) + '.cache')

    def put(self, key, value):
        with open(self._getpath(key), 'wb') as f:
            f.write(zlib.compress(pickle.dumps(value, -1)))
        self._cache[key] = value

    def get(self, key):
        if key in self._cache:
            return self._cache[key]

        try:
            with open(self._getpath(key), 'rb') as f:
                return pickle.loads(zlib.decompress(f.read()))
        except IOError as ex:
            pyfalog.debug("IO error opening zip file. (May not exist yet)")
            if ex.errno == 2:  # file does not exist (yet)
                return None
            else:
                raise

    def invalidate(self, key):
        self._cache.pop(key, None)

        try:
            os.unlink(self._getpath(key))
        except OSError as ex:
            pyfalog.debug("Caught exception in invalidate")
            pyfalog.debug(ex)
            if ex.errno == 2:  # does not exist
                pass
            else:
                raise


class DictCache(APICache):
    def __init__(self):
        self._dict = {}

    def get(self, key):
        return self._dict.get(key, None)

    def put(self, key, value):
        self._dict[key] = value

    def invalidate(self, key):
        self._dict.pop(key, None)


class APIConnection(object):
    def __init__(self, additional_headers=None, user_agent=None, cache_dir=None, cache=None):
        # Set up a Requests Session
        session = requests.Session()
        if additional_headers is None:
            additional_headers = {}
        if user_agent is None:
            user_agent = "pyfa/{0} ({1})".format(config.version, config.tag)
        session.headers.update({
            "User-Agent": user_agent,
            "Accept": "application/json",
        })
        session.headers.update(additional_headers)
        session.mount('https://public-crest.eveonline.com', HTTPAdapter())
        self._session = session
        if cache:
            if isinstance(cache, APICache):
                self.cache = cache  # Inherit from parents
            elif isinstance(cache, type):
                self.cache = cache()  # Instantiate a new cache
        elif cache_dir:
            self.cache_dir = cache_dir
            self.cache = FileCache(self.cache_dir)
        else:
            self.cache = DictCache()

    def get(self, resource, params=None):
        pyfalog.debug('Getting resource {0}', resource)
        if params is None:
            params = {}

        # remove params from resource URI (needed for paginated stuff)
        parsed_uri = urlparse(resource)
        qs = parsed_uri.query
        resource = urlunparse(parsed_uri._replace(query=''))
        prms = {}
        for tup in parse_qsl(qs):
            prms[tup[0]] = tup[1]

        # params supplied to self.get() override parsed params
        for key in params:
            prms[key] = params[key]

        # check cache
        key = (resource, frozenset(self._session.headers.items()), frozenset(prms.items()))
        cached = self.cache.get(key)
        if cached and cached['cached_until'] > time.time():
            pyfalog.debug('Cache hit for resource {0} (params={1})', resource, prms)
            return cached
        elif cached:
            pyfalog.debug('Cache stale for resource {0} (params={1})', resource, prms)
            self.cache.invalidate(key)
        else:
            pyfalog.debug('Cache miss for resource {0} (params={1})', resource, prms)

        pyfalog.debug('Getting resource {0} (params={1})', resource, prms)
        res = self._session.get(resource, params=prms)
        if res.status_code != 200:
            raise APIException("Got unexpected status code from server: {0}" % res.status_code)

        ret = res.json()

        # cache result
        expires = self._get_expires(res)
        if expires > 0:
            ret.update({'cached_until': time.time() + expires})
            self.cache.put(key, ret)

        return ret

    @staticmethod
    def _get_expires(response):
        if 'Cache-Control' not in response.headers:
            return 0
        if any([s in response.headers['Cache-Control'] for s in ['no-cache', 'no-store']]):
            return 0
        match = cache_re.search(response.headers['Cache-Control'])
        if match:
            return int(match.group(1))
        return 0


class EVE(APIConnection):
    def __init__(self, **kwargs):
        self.api_key = kwargs.pop('api_key', None)
        self.client_id = kwargs.pop('client_id', None)
        self.redirect_uri = kwargs.pop('redirect_uri', None)
        if kwargs.pop('testing', False):
            self._public_endpoint = "http://public-crest-sisi.testeveonline.com/"
            self._authed_endpoint = "https://api-sisi.testeveonline.com/"
            self._image_server = "https://image.testeveonline.com/"
            self._oauth_endpoint = "https://sisilogin.testeveonline.com/oauth"
        else:
            self._public_endpoint = "https://public-crest.eveonline.com/"
            self._authed_endpoint = "https://crest-tq.eveonline.com/"
            self._image_server = "https://image.eveonline.com/"
            self._oauth_endpoint = "https://login.eveonline.com/oauth"
        self._endpoint = self._public_endpoint
        self._cache = {}
        self._data = None
        self.token = None
        self.refresh_token = None
        self.expires = None
        APIConnection.__init__(self, **kwargs)

    def __call__(self):
        if not self._data:
            self._data = APIObject(self.get(self._endpoint), self)
        return self._data

    def __getattr__(self, item):
        return self._data.__getattr__(item)

    def auth_uri(self, scopes=None, state=None):
        s = [] if not scopes else scopes
        grant_type = "token" if self.api_key is None else "code"

        return "%s/authorize?response_type=%s&redirect_uri=%s&client_id=%s%s%s" % (
            self._oauth_endpoint,
            grant_type,
            self.redirect_uri,
            self.client_id,
            "&scope=%s" % '+'.join(s) if scopes else '',
            "&state=%s" % state if state else ''
        )

    def _authorize(self, params):
        auth = text_(base64.b64encode(bytes_("%s:%s" % (self.client_id, self.api_key))))
        headers = {"Authorization": "Basic %s" % auth}
        res = self._session.post("%s/token" % self._oauth_endpoint, params=params, headers=headers)
        if res.status_code != 200:
            raise APIException("Got unexpected status code from API: %i" % res.status_code)
        return res.json()

    def set_auth_values(self, res):
        self.__class__ = AuthedConnection
        self.token = res['access_token']
        self.refresh_token = res['refresh_token']
        self.expires = int(time.time()) + res['expires_in']
        self._endpoint = self._authed_endpoint
        self._session.headers.update({"Authorization": "Bearer %s" % self.token})

    def authorize(self, code):
        res = self._authorize(params={"grant_type": "authorization_code", "code": code})
        self.set_auth_values(res)

    def refr_authorize(self, refresh_token):
        res = self._authorize(params={"grant_type": "refresh_token", "refresh_token": refresh_token})
        self.set_auth_values(res)

    def temptoken_authorize(self, access_token=None, expires_in=0, refresh_token=None):
        self.set_auth_values({'access_token': access_token,
                              'refresh_token': refresh_token,
                              'expires_in': expires_in})


class AuthedConnection(EVE):
    def __call__(self):
        if not self._data:
            self._data = APIObject(self.get(self._endpoint), self)
        return self._data

    def whoami(self):
        # if 'whoami' not in self._cache:
        #    print "Setting this whoami cache"
        #    self._cache['whoami'] = self.get("%s/verify" % self._oauth_endpoint)
        return self.get("%s/verify" % self._oauth_endpoint)

    def get(self, resource, params=None):
        if self.refresh_token and int(time.time()) >= self.expires:
            self.refr_authorize(self.refresh_token)
        return super(self.__class__, self).get(resource, params)

    def post(self, resource, data, params=None):
        if self.refresh_token and int(time.time()) >= self.expires:
            self.refr_authorize(self.refresh_token)
        return self._session.post(resource, data=data, params=params)

    def delete(self, resource, params=None):
        if self.refresh_token and int(time.time()) >= self.expires:
            self.refr_authorize(self.refresh_token)
        return self._session.delete(resource, params=params)


class APIObject(object):
    def __init__(self, parent, connection):
        self._dict = {}
        self.connection = connection
        for k, v in parent.items():
            if type(v) is dict:
                self._dict[k] = APIObject(v, connection)
            elif type(v) is list:
                self._dict[k] = self._wrap_list(v)
            else:
                self._dict[k] = v

    def _wrap_list(self, list_):
        new = []
        for item in list_:
            if type(item) is dict:
                new.append(APIObject(item, self.connection))
            elif type(item) is list:
                new.append(self._wrap_list(item))
            else:
                new.append(item)
        return new

    def __getattr__(self, item):
        if item in self._dict:
            return self._dict[item]
        raise AttributeError(item)

    def __call__(self, **kwargs):
        # Caching is now handled by APIConnection
        if 'href' in self._dict:
            return APIObject(self.connection.get(self._dict['href'], params=kwargs), self.connection)
        else:
            return self

    def __str__(self):  # pragma: no cover
        return self._dict.__str__()

    def __repr__(self):  # pragma: no cover
        return self._dict.__repr__()

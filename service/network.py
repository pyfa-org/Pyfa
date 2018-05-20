# =============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import requests
import socket
from logbook import Logger

import config
from service.settings import NetworkSettings

pyfalog = Logger(__name__)

# network timeout, otherwise pyfa hangs for a long while if no internet connection
timeout = 3
socket.setdefaulttimeout(timeout)


class Error(Exception):
    def __init__(self, msg=None):
        self.message = msg


class RequestError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class ServerError(Exception):
    pass


class TimeoutError(Exception):
    pass


class Network(object):
    # Request constants - every request must supply this, as it is checked if
    # enabled or not via settings
    ENABLED = 1
    EVE = 2  # Mostly API, but also covers CREST requests. update: might be useless these days, this Network class needs to be reviewed
    PRICES = 4
    UPDATE = 8

    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Network()

        return cls._instance

    def request(self, url, type, *args, **kwargs):

        # URL is required to be https as of right now
        # print "Starting request: %s\n\tType: %s\n\tPost Data: %s"%(url,type,data)

        # Make sure request is enabled
        access = NetworkSettings.getInstance().getAccess()

        if not self.ENABLED & access or not type & access:
            pyfalog.warning("Access not enabled - please enable in Preferences > Network")
            raise Error("Access not enabled - please enable in Preferences > Network")

        # Set up some things for the request
        versionString = "{0} {1} - {2} {3}".format(config.version, config.tag, config.expansionName,
                                                   config.expansionVersion)
        headers = {"User-Agent": "pyfa {0} (python-requests {1})".format(versionString, requests.__version__)}
        # user-agent: pyfa 2.0.0b4 git -YC120.2 1.2 (python-requests 2.18.4)

        # python-requests supports setting proxy for request as parameter to get() / post()
        # in a form like: proxies = { 'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080' }
        # or with HTTP Basic auth support: proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
        # then you do: requests.get('http://example.org', proxies=proxies)

        proxies = NetworkSettings.getInstance().getProxySettingsInRequestsFormat()

        try:
            resp = requests.get(url, headers=headers, proxies=proxies, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.exceptions.HTTPError as error:
            pyfalog.warning("HTTPError:")
            pyfalog.warning(error)
            if error.response.status_code == 404:
                raise RequestError()
            elif error.response.status_code == 403:
                raise AuthenticationError()
            elif error.response.status_code >= 500:
                raise ServerError()
            raise Error(error)
        except requests.exceptions.Timeout:
            raise TimeoutError()
        except Exception as error:
            raise Error(error)

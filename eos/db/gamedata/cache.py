import eos.config

configVal = getattr(eos.config, "gamedataCache", None)
if configVal is True:
    def cachedQuery(amount, *keywords):
        def deco(function):
            cache = {}

            def checkAndReturn(*args, **kwargs):
                useCache = kwargs.pop("useCache", True)
                cacheKey = []
                cacheKey.extend(args)
                for keyword in keywords:
                    cacheKey.append(kwargs.get(keyword))

                cacheKey = tuple(cacheKey)
                handler = cache.get(cacheKey)
                if handler is None or not useCache:
                    handler = cache[cacheKey] = function(*args, **kwargs)

                return handler

            return checkAndReturn

        return deco

elif callable(configVal):
    cachedQuery = eos.config.gamedataCache
else:
    def cachedQuery(amount, *keywords):
        def deco(function):
            def checkAndReturn(*args, **kwargs):
                return function(*args, **kwargs)

            return checkAndReturn

        return deco

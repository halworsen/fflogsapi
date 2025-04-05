from functools import wraps


def fetch_data(*keys):
    '''
    Decorator that queries and stores the given `key` in a class's `_data` dictionary.

    The class must have a `_data` dictionary field and a `_query_data` function which
    queries for the data specified by the `key`. The class must also have a `DATA_INDICES` field
    which is a list describing how to index into the relevant data.

    Args:
        `key`: The key to query and store.
    '''
    def decorator(func):
        @wraps(func)
        def ensured(*args, **kwargs):
            self = args[0]
            for key in keys:
                if key not in self._data:
                    result = self._query_data(key)
                    self._data[key] = result[key]
            return func(*args, **kwargs)
        return ensured
    return decorator


def default_instantiation(_class):
    '''
    Class decorator which instantiates the class with dunder defaults when no args are given on
    instantiation.
    '''
    def instantiator(*args, **kwargs):
        if not args and not kwargs:
            if hasattr(_class, '__default_args__'):
                args = _class.__default_args__
            if hasattr(_class, '__default_kwargs__'):
                kwargs = _class.__default_kwargs__
        return _class(*args, **kwargs)
    return instantiator

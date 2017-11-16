"""Property decorators."""


class cachedproperty:
    """Decorator to a class method a cached property.

    The property method is called just the first time for an instance, and its
    result cached.

    """

    def __init__(self, func):
        self._func = func
        self._name = func.__name__

    def __get__(self, instance, owner):
        value = self._func(instance)
        # The property itself is replaced with the result of the function call
        setattr(instance, self._name, value)
        return value

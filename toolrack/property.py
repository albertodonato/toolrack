"""Property decorators."""

from typing import (
    Any,
    Callable,
)


class cachedproperty:
    """Decorator to a class method a cached property.

    The property method is called just the first time for an instance, and its
    result cached.

    """

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self._func = func
        self._name = func.__name__

    def __get__(self, instance: Any, owner: Any) -> Any:
        value = self._func(instance)
        # The property itself is replaced with the result of the function call
        setattr(instance, self._name, value)
        return value

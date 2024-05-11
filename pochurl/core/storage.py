import functools
import logging
from abc import ABC, abstractmethod
from typing import List

from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


class Storage(ABC):

    @abstractmethod
    def read_item(self, id: str) -> SavedElement | None:
        pass

    @abstractmethod
    def read_items(self) -> List[SavedElement]:
        pass

    @abstractmethod
    def read_items_by_name(self, name: str) -> List[SavedElement]:
        pass

    @abstractmethod
    def read_items_by_url(self, url: AnyHttpUrl) -> List[SavedElement]:
        pass

    @abstractmethod
    def write_item(self, element: GivenElement) -> str:
        pass

    @abstractmethod
    def rewrite_item(self, id: str, element: GivenElement) -> str | None:
        pass


def log(_func=None, *, logger: logging.Logger):
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
            signature = ', '.join(args_repr[1:] + kwargs_repr)
            logger.info(f'function {func.__name__} called with args `{signature}`')
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(f'Exception raised in {func.__name__}. exception: {str(e)}')
                raise e
        return wrapper

    if _func is None:
        return decorator_log
    return decorator_log(_func)

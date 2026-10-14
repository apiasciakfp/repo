from abc import ABC, abstractmethod


class IParseStrategy(ABC):
    @abstractmethod
    def separator(self) -> str: ...

    @abstractmethod
    def split_into_records(self, order_string: str) -> list[str]: ...

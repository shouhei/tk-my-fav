from abc import ABCMeta
from abc import abstractmethod
from requests import Response
from lib.cell_data import CellData
from typing import Iterator


class AbstractDataSource(metaclass=ABCMeta):
    def __init__(self):
        pass

    @classmethod
    def endpoint(cls) -> str:
        """
        :rtype: str
        :return: endpoint url
        """
        return cls._ENDPOINT

    @abstractmethod
    def _get(self) -> Response:
        """
        データを実際に取得するメソッド。
        基本的に外部からは呼ばない。
        :rtype: Response
        :return: Response is from requests
        """
        pass

    @abstractmethod
    def each(self) -> Iterator[CellData]:
        """
        取得したデータをCellDataとしてジェネレートする。
        :rtype: Iterable[CellData]
        :return: any data
        """
        pass
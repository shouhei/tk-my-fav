from lib.cell_data import CellData
from lib.datasource.abstract.abstract_data_source import AbstractDataSource
from datetime import datetime
from typing import Iterator


class Dummy(AbstractDataSource):
    """
    開発用のダミーデータクラス
    """

    def __init__(self):
        self.__dummy = [x for x in range(20)]

    def _get(self):
        pass

    def each(self) -> Iterator[CellData]:
        """
        ダミーデータを20件、CellDataとしてジェネレートする。

        :rtype: Iterable[CellData]
        :return: dummy data
        """
        for row in self.__dummy:
            yield CellData(
                    datetime.now(),
                    text='this is dummy text',
                    url='https://google.co.jp',
                    image='http://blog-imgs-31.fc2.com/0/4/9/0497/nagogazo156.jpg'
            )
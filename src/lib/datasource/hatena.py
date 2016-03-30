from lib.cell_data import CellData
from lib.datasource.abstract.abstract_data_source import AbstractDataSource
from datetime import datetime
from string import Template
import xml.etree.ElementTree as ET
import requests
from typing import Iterator


class Hatena(AbstractDataSource):
    """
    はてなのRSSから特定ユーザーのブックマークを取得するクラス
    """
    _ENDPOINT=Template("http://b.hatena.ne.jp/$user_name/rss")

    def __init__(self, user_name: str):
        """
        :param struser_name: hatena bookmark user name
        """
        self.__user_name = user_name
        self.__data_raw = self._get().text


    def endpoint(self):
        """
        はてなのエンドポイントはユーザーによって変わるのでAbstractDataSourceからオーバーライド

        :rtype: str
        :return: end point
        """
        return self._ENDPOINT.substitute(user_name=self.__user_name)

    def _get(self):
        """
        データを実際に取得するメソッド。

        基本的に外部からは呼ばない。

        :rtype: Response
        :return: Response is from requests
        """
        return requests.get(url=self.endpoint())

    def each(self) -> Iterator[CellData]:
        """
        取得したデータをCellDataとしてジェネレートする。

        :rtype: Iterator[CellData]
        :return: hatena bookmark data
        """
        tree = ET.fromstring(self.__data_raw)
        for item in tree[1:]:
            yield CellData(
                    datetime.strptime(item[5].text, "%Y-%m-%dT%H:%M:%S+09:00"),
                    text=item[0].text,
                    url=item[1].text,
                    image=None
            )


if __name__ == "__main__":
    from config.hatena import USER_NAME
    h = Hatena(USER_NAME)
    for i in h.each():
        print(i)

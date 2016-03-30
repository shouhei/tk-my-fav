from typing import List
from lib.cell_data import CellData
from lib.datasource.abstract.abstract_data_source import AbstractDataSource


class DataSourceManager(object):
    """
    各種データソースをまとめるクラス
    TODO: 実データのリスト(self.__data)が別クラスになっているべき
    """
    def __init__(self, data_source_list: List[AbstractDataSource]=[], order_by: str=None):
        """
        :param List data_source_list: データソースのリスト
        :param str order_by: データの順番を決定する項目
        """
        self.__data = []
        self.__data_source_list = data_source_list
        self.__order_by = order_by
        self.get(refresh=True)

    @property
    def order_by(self):
        """
        :rtype: str
        :return: データの並び順を決定するプロパティを返す
        """
        return self.order_by

    @order_by.setter
    def order_by(self, order_by):
        """
        :param order_by: データの並び順を決定するプロパティ
        """
        self.__order_by = order_by
        self.update()

    def update(self):
        """
        get の refresh引数がTrueのエイリアス
        """
        self.get(refresh=True)

    def get(self, refresh: bool=False) -> List[CellData]:
        """
        TODO: if self.__order_by の箇所は別クラスが持つべき
        :param bool refresh: データを更新するか否か
        :rtype: List[CellData]
        :return: 実データの入ったリストを返す
        """
        if refresh:
            self.__data = []
            for obj in self.__data_source_list:
                for data in obj.each():
                    self.__data.append(data)
        if self.__order_by:
            return reversed(sorted(self.__data, key=lambda o, method=self.__order_by: getattr(o, method)))
        else:
            return self.__data

    def register(self, obj: AbstractDataSource):
        """
        :param AbstractDataSource obj: データソースを追加する
        """
        self.__data_source_list.append(obj)
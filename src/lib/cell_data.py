from datetime import datetime


class CellData(object):
    """
    api や rss を叩いて取得したデータを、このクラスに詰めて、各データを均一化する
    """
    def __init__(self, date: datetime, text: str=None, url: str=None, image: str=None):
        """
        :param datetime date: data's created date
        :param str text: main text
        :param str url: url
        :param str image: image url
        """
        self.__date = date
        self.__text = text
        self.__url = url
        self.__image = image

    @property
    def text(self):
        return self.__text

    @property
    def url(self):
        return self.__url

    @property
    def image(self):
        return self.__image

    @property
    def date(self):
        return self.__date

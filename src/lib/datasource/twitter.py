from requests_oauthlib import OAuth1Session
from lib.cell_data import CellData
from lib.datasource.abstract.abstract_data_source import AbstractDataSource
from datetime import datetime
from typing import Iterable
from requests import Response


class Twitter(AbstractDataSource):
    """
    Twitter の like を取得するクラス
    """
    _ENDPOINT = "https://api.twitter.com/1.1/favorites/list.json"

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        """
        :param str consumer_key: twitter consumer key
        :param str consumer_secret: twitter consumer secret
        :param str access_token: twitter access token
        :param str acces_secret: tiwtter access secret
        """
        self.__requester = OAuth1Session(
                consumer_key,
                consumer_secret,
                access_token,
                access_secret
        )
        self.__data_raw = self._get()

    def _get(self) -> Response:
        """
        データを実際に取得するメソッド。
        基本的に外部からは呼ばない。
        :rtype: Response
        :return: Response is from requests
        """
        return self.__requester.get(url=self.endpoint())

    def each(self) -> Iterable[CellData]:
        """
        取得したデータをCellDataとしてジェネレートする。
        :rtype: Iterable[CellData]
        :return: twitter liked data
        """
        if self.__data_raw.status_code != 200:
            print(self.__data_raw.status_code)
            return None
        for row in self.__data_raw.json():
            yield CellData(
                    datetime.strptime(str(row['created_at']), "%a %b %d %H:%M:%S +0000 %Y"),
                    text=row['text'],
                    url=row['entities']['urls'][0]['expanded_url'] if len(row['entities']['urls']) > 0 else '',
                    image=row['extended_entities']['media'][0]['media_url_https'] if 'extended_entities' in row and len(row['extended_entities']) > 0 else ''
            )


if __name__ == '__main__':
    from config.twitter import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
    from string import Template
    t = Twitter(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    template = Template("text: $text\nurl: $url\ndate: $date\nimage: $image")
    for data in t.each():
        print(template.substitute(text=data.text, url=data.url, date=data.date, image=data.image))

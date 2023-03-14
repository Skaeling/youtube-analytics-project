import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    data_list = []

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        Channel.data_list.append(self.__dict__)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """класс-метод `get_service()`, возвращающий объект для работы с YouTube API"""
        return cls.youtube

    @staticmethod
    def to_json(path="../homework-2/vdud.json"):
        """- метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        with open(path, 'w') as outfile:
            for s in Channel.data_list:
                json.dump(s, outfile, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

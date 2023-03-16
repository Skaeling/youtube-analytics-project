import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Возвращает название и ссылку на канал
        по шаблону `<название_канала> (<ссылка_на_канал>)`"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Реализует возможность складывать два канала между собой по количеству подписчиков"""
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """Реализует возможность вычитать количество подписчиков одного канала из другого"""
        return self.subscribers - other.subscribers

    def __ge__(self, other):
        """Реализует возможность сравнивать два канала между собой по количеству подписчиков"""
        return self.subscribers >= other.subscribers

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """класс-метод `get_service()`, возвращающий объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, path="../homework-2/vdud.json"):
        """- метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        with open(path, 'w') as outfile:
            json.dump(self.__dict__, outfile, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

import json
import os

from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY_YT')
# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        cannel = json.dumps(youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2, ensure_ascii=False)
        print(cannel)

    @classmethod
    def get_service(cls, channel_id):
        '''
        - id канала
        - название канала
        - описание канала
        - ссылка на канал
        - количество подписчиков
        - количество видео
        - общее количество просмотров
        '''
        playlists = (youtube.channels().list(id=channel_id, part='snippet,statistics').execute())

        for playlist in playlists["items"]:
            id = playlist['id']
            title = playlist['snippet']['title']
            description = playlist['snippet']['description']
            url = playlist['snippet']['thumbnails']['default']['url']
            subscribers = playlist['statistics']['subscriberCount']
            videos = playlist['statistics']['videoCount']
            views = playlist['statistics']['viewCount']
        return cls(id, title, description, url, subscribers, videos, views)









moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
moscowpython.get_service('UC-OVMPlMA3-YCIeg4z5z23A')














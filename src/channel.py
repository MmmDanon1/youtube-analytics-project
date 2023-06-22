import json
import os

from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY_YT')
# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id = None, id = None, title = None, description = None, url = None, subscribers = None, video_count = None, views = None) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.subscribers = subscribers
        self.video_count = video_count
        self.views = views

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        cannel = json.dumps(youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2, ensure_ascii=False)
        print(cannel)

    @classmethod
    def get_service(cls, channel_id):
        '''
        Получение:
        - id канала
        - название канала
        - описание канала
        - ссылка на канал
        - количество подписчиков
        - количество видео
        - общее количество просмотров
        '''
        playlists = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        for playlist in playlists['items']:
            id = playlist['id']
            title = playlist['snippet']['title']
            description = playlist['snippet']['description']
            url = playlist['snippet']['thumbnails']['default']['url']
            subscribers = playlist['statistics']['subscriberCount']
            video_count = playlist['statistics']['videoCount']
            views = playlist['statistics']['viewCount']
        return cls(id, title, description, url, subscribers, video_count, views)

    def to_json(self, title):
        """
        Создание файла JSON
        """
        with open(f'{title.lower()}', 'a') as f:
            json.dump([str(self)], f)























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
        playlists = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        for playlist in playlists['items']:
            self.id = playlist['id']
            self.title = playlist['snippet']['title']
            self.description = playlist['snippet']['description']
            self.url = playlist['snippet']['thumbnails']['default']['url']
            self.subscribers = int(playlist['statistics']['subscriberCount'])
            self.video_count = int(playlist['statistics']['videoCount'])
            self.views = int(playlist['statistics']['viewCount'])

    def __str__(self):
        """
        возвращаtn название и ссылку на канал по шаблону `<название_канала> (<ссылка_на_канал>)
        """
        return f"Название канала: {self.subscribers}, ссылка на канал: {self.url}"

    def __add__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (сложение)
        """
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (вычитание)
        """
        return self.subscribers - other.subscribers

    def __lt__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (меньше ли)
        """
        return self.subscribers < other.subscribers

    def __le__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (меньше или ровно)
        """
        return self.subscribers <= other.subscribers

    def __gt__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (больше ли)
        """
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        """
        сравниваtn два канала между собой по числу подписчиков (больше или ровно)
        """
        return self.subscribers >= other.subscribers

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























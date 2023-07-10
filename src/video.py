import os

from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY_YT')
# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)
class Video:

    def __init__(self, video_id: str) -> None:
        """
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков
        """
        try:
            self.video_id = video_id
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        except IndexError:
            self.video_id = video_id
            self.video_title: str = None
            self.view_count: int = None
            self.like_count: int = None
            self.comment_count: int = None



    def __str__(self):
        """
        возвращает название канала
        """
        return self.video_title

class PLVideo(Video):

    def __init__(self, id_video: str,  id_playlist: str):
        """
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков
        - id плейлиста
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist








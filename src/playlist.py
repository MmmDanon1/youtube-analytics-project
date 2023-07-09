import isodate
from googleapiclient.discovery import build
from datetime import timedelta

import os

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY_YT')
# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList:
    """
    класс, который инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
  - название плейлиста
  - ссылку на плейлист
  - суммарная длительность видео
    """
    time_video = []
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        for video in playlist_videos['items']:
            self.title = video['snippet']['title'][0:24]

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_ids
                                               ).execute()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            PlayList.time_video.append(str(duration))
        self.__total_duration = timedelta()
        for i in PlayList.time_video:
            (h, m, s) = i.split(':')
            d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            self.__total_duration += d

    @property
    def total_duration(self):
        return self.__total_duration
    #
    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        like_video = []
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_ids
                                               ).execute()
        for like_count in video_response['items']:
            like_video.append(int(like_count['statistics']['likeCount']))
            max_like = max(like_video)
            index = like_video.index(max_like)

        return f"https://youtu.be/{video_ids[index]}"















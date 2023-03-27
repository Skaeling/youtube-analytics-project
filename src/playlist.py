from src.channel import Channel
import datetime
import isodate


class PlayList:
    def __init__(self, playlist_id):
        self.delta = None
        self.playlist_id = playlist_id
        self.playlist_videos = Channel.youtube.playlists().list(id=playlist_id,
                                                                part='contentDetails, snippet',
                                                                maxResults=50, ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста"""
        playlist_videos = Channel.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                               part='contentDetails',
                                                               maxResults=50,
                                                               ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = Channel.youtube.videos().list(part='contentDetails,statistics',
                                                       id=','.join(video_ids)
                                                       ).execute()
        self.delta = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.delta += duration
        return self.delta

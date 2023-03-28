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
        self.playlist_item_list = Channel.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_item_list['items']]
        self.video_response = Channel.youtube.videos().list(part='contentDetails,statistics',
                                                            id=','.join(self.video_ids)
                                                            ).execute()

    @property
    def total_duration(self) -> object:
        """Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста"""
        self.delta = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.delta += duration
        return self.delta

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        most_fav = []
        for video in self.video_response['items']:
            fav = video['statistics']["likeCount"]
            most_fav.append(int(fav))
        result = max(most_fav)
        for video in self.video_response['items']:
            if int(video['statistics']["likeCount"]) == result:
                best_vid = video['id']
                return f'https://youtu.be/{best_vid}'

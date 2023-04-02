from src.channel import Channel
from googleapiclient.errors import HttpError


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                id=self.video_id
                                                                ).execute()
        except HttpError as e:
            print(e.status_code.self.video_response)
            print(e.reason.self.video_response)
            print(e.error_details.self.video_response)
        else:
            if not self.video_response['items']:
                self.title = None
                self.view_count = None
                self.like_count = None
                self.video_url = None

            else:
                self.title = self.video_response['items'][0]['snippet']['title']
                self.view_count = self.video_response['items'][0]['statistics']['viewCount']
                self.like_count = self.video_response['items'][0]['statistics']['likeCount']
                self.video_url = self.video_response['items'][0]['snippet']['thumbnails']['default']['url']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

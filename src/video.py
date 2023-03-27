from src.channel import Channel


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=self.video_id
                                                            ).execute()
        self.video_name = self.video_response['items'][0]['snippet']['title']
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        self.video_url = self.video_response['items'][0]['snippet']['thumbnails']['default']['url']

    def __str__(self):
        return f'{self.video_name}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

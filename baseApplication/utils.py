import instaloader
from googleapiclient.discovery import build
from django.conf import settings

def fetch_youtube_channel_data(channel_url):
    # Initialize the YouTube Data API client
    api_key = settings.YOUTUBE_API_KEY
    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_id = channel_url.split('/')[-1]
    try:
        # Call the channels.list method to retrieve channel statistics
        details_response = youtube.channels().list(
            part='statistics,snippet,contentDetails',
            id=channel_id
        ).execute()

        if 'items' in details_response:
            channel = details_response['items'][0]
            snippet = channel['snippet']
            statistics = channel['statistics']
            uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

            channel_title = snippet.get('title', '')
            creation_date = snippet.get('publishedAt', '')
            views = statistics.get('viewCount', 0)
            subscribers = statistics.get('subscriberCount', 0)
            videos = statistics.get('videoCount', 0)

            # Initialize totals
            total_likes = 0
            total_comments = 0

            # Retrieve all videos in the uploads playlist
            next_page_token = None
            while True:
                playlist_response = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]

                # Get statistics for each video
                video_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(video_ids)
                ).execute()

                for video in video_response['items']:
                    video_stats = video['statistics']
                    total_likes += int(video_stats.get('likeCount', 0))
                    total_comments += int(video_stats.get('commentCount', 0))

                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break

            channel_data = {
                'likes': total_likes,
                'views': views,
                'subscribers': subscribers,
                'comments': total_comments,
                'videos': videos,
                'channel_title': channel_title,
                'creation_date': creation_date
            }
            return channel_data

        else:
            print('No items found in YouTube API response:', details_response)
            return None
    except Exception as e:
        print('An error occurred while fetching YouTube data:', e)
        return None


def fetch_instagram_profile(username):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        profile_data = {
            'username': profile.username,
            'full_name': profile.full_name,
            'followers': profile.followers,
            'following': profile.followees,
            'posts': profile.mediacount,
            'total_likes': get_total_likes(profile)
        }
        return profile_data
    except instaloader.exceptions.ProfileNotExistsException:
        return {'error': f'Profile "{username}" does not exist.'}
    except instaloader.exceptions.LoginRequiredException:
        return {'error': f'Login required to access profile "{username}".'}
    except Exception as e:
        return {'error': str(e)}

def get_total_likes(profile):
    total_likes = 0
    for post in profile.get_posts():
        total_likes += post.likes
    return total_likes

import json

import requests
from pyyoutube import Api


def get_data(api_key, video_id, maxResults, nextPageToken):
    url = 'https://www.googleapis.com/youtube/v3/commentThreads?key={KEY}&textFormat=plainText&' + \
                  'part=snippet&video_id={video_id}&maxResults={maxResults}&pageToken={nextPageToken}'
    format_url = url.format(KEY=api_key,
                                            videoId=video_id,
                                            maxResults=maxResults,
                                            nextPageToken=nextPageToken)
    return json.loads(requests.get(format_url).text)


def get_text_of_comment(data):
    comments = set()
    for item in data['items']:
        comments.add(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    return comments


def get_all_comments(api_key, query):
    api = Api(api_key=api_key)
    video_by_keywords = api.search_by_keywords(q=query,
                                               search_type=["video"],
                                               count=10,
                                               limit=30)
    video_id = [x.id.video_id for x in video_by_keywords.items]

    comments_all = []
    for video in video_id:
        data = get_data(api_key,
                        video,
                        maxResults=10,
                        nextPageToken='')
        comments_all.append(list(get_text_of_comment(data)))
    comments = sum(comments_all, [])
    return comments

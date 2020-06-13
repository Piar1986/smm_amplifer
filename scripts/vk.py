import requests
import datetime
from .start_date import calculate_start_date


def determine_group_id(group_name, access_token, version):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id':group_name,
        'access_token':access_token, 
        'v':version
    }
    response = requests.get(url, params=params)
    response_result = response.json()
    if 'error' in response_result:
        raise requests.exceptions.HTTPError(response_result['error'])
    group_id = response_result['response'][0]['id']
    return group_id


def get_posts(group_id, access_token, version):
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id':f'-{group_id}',
        'access_token':access_token, 
        'v':version
    }
    response = requests.get(url, params=params)
    response_result = response.json()
    if 'error' in response_result:
        raise requests.exceptions.HTTPError(response_result['error'])
    posts = response_result['response']['items']
    return posts


def get_post_comments(post_id, group_id, access_token, version):
    url = 'https://api.vk.com/method/wall.getComments'
    page = 0
    pages_number = 1
    page_comments_count = 100
    post_comments = []
    
    while page <= pages_number:
        params = {
            'owner_id':f'-{group_id}',
            'post_id':post_id,
            'count':page_comments_count,
            'offset':page,
            'access_token':access_token, 
            'v':version
        }
        response = requests.get(url, params=params)
        response_result = response.json()
        if 'error' in response_result:
            raise requests.exceptions.HTTPError(response_result['error'])
        comments = response_result['response']['items']
        post_comments.extend(comments)

        comments_count = response_result['response']['count']
        pages_number = comments_count // page_comments_count
        page += 1

    return post_comments


def get_comments_users_ids(comments, start_date, group_id):
    post_comments_users_ids = []
    for comment in comments:
        timestamp = comment['date']
        comment_date = datetime.datetime.utcfromtimestamp(timestamp)
        if comment_date < start_date:
            continue
        user_id = comment['from_id']
        owner_id = f'-{group_id}'
        if user_id==owner_id:
        	continue
        post_comments_users_ids.append(user_id)
    return post_comments_users_ids


def get_post_likes(post_id, group_id, access_token, version):
    url = 'https://api.vk.com/method/likes.getList'
    page = 0
    pages_number = 1
    page_likes_count = 100
    post_likes = []
    while page <= pages_number:
        params = {
            'type':'post',
            'owner_id':f'-{group_id}',
            'item_id':post_id,
            'count': page_likes_count,
            'offset': page,
            'access_token':access_token, 
            'v':version
        }
        response = requests.get(url, params=params)
        response_result = response.json()
        if 'error' in response_result:
            raise requests.exceptions.HTTPError(response_result['error'])
        likes = response_result['response']['items']
        post_likes.extend(likes)

        likes_count = response_result['response']['count']
        pages_number = likes_count // page_likes_count
        page += 1

    return post_likes


def fetch_vk_analyze(access_token, version, days_count, months_count, group_name):
    group_id = determine_group_id(
        group_name,
        access_token,
        version,
        )
    posts = get_posts(
        group_id, 
        access_token, 
        version,
        )
    posts_ids = [post['id'] for post in posts]

    posts_comments = []
    posts_likers = []
    for post in posts_ids:
        post_comments = get_post_comments(
            post, 
            group_id, 
            access_token, 
            version,
            )
        posts_comments.extend(post_comments)
        post_likers = get_post_likes(
            post, 
            group_id, 
            access_token, 
            version
            )
        posts_likers.extend(post_likers)

    start_date = calculate_start_date(days_count, months_count)
    comments_users_ids = get_comments_users_ids(
        posts_comments, 
        start_date, 
        group_id
        )
    
    commentators_ids = set(comments_users_ids)
    likers_ids = set(posts_likers)
    audience_core = commentators_ids & likers_ids
    print('Audience core:', audience_core)
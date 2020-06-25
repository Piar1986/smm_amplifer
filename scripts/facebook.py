import requests
from .start_date import calculate_start_date


def get_groups(access_token, user_id):
    url = f"https://graph.facebook.com/{user_id}/groups"
    params = {'access_token':access_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_result = response.json()
    groups = response_result['data']
    return groups


def get_group_posts(access_token, group_id):
    url = f"https://graph.facebook.com/{group_id}/feed"
    params = {
        'access_token':access_token,
        'fields': 'message'
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_result = response.json()
    group_posts = response_result['data']
    return group_posts


def get_post_comments(access_token, post_id, start_date):
    url = f"https://graph.facebook.com/{post_id}/comments"
    params = {
        'access_token':access_token,
        'since':start_date
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_result = response.json()
    post_comments = response_result['data']
    return post_comments


def get_posts_comments(access_token, posts_ids, start_date):
    posts_comments = []
    for post in posts_ids:
        post_comments = get_post_comments(access_token, post, start_date)
        posts_comments.extend(post_comments)
    return posts_comments


def get_post_reactions(access_token, post_id):
    url = f"https://graph.facebook.com/{post_id}/reactions"
    params = {'access_token':access_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_result = response.json()
    post_reactions = response_result['data']
    return post_reactions


def get_posts_reactions(access_token, posts_ids):
    posts_reactions = []
    for post_id in posts_ids:
        post_reactions = get_post_reactions(access_token, post_id)
        posts_reactions.extend(post_reactions)
    return posts_reactions


def get_user_reactions_statistic(user_id, reactions, facebook_reactions):
    user_reactions_statistic = {}
    for reaction in facebook_reactions:
        user_reactions = [reaction['type'] for reaction in reactions if user_id==reaction['id']]
        reactions_count = user_reactions.count(reaction)
        user_reactions_statistic[reaction] = reactions_count
    return user_reactions_statistic


def fetch_facebook_analyze(access_token, user_id, days_count, months_count, facebook_reactions, group_name):
    groups = get_groups(access_token, user_id)
    group_id = [group['id'] for group in groups if group['name']==group_name][0]
    group_posts = get_group_posts(access_token, group_id)
    posts_ids = [post['id'] for post in group_posts]
    start_date = calculate_start_date(days_count, months_count)
    posts_comments = get_posts_comments(
        access_token, 
        posts_ids, 
        start_date,
        )
    commentators_ids = set([comment['from']['id'] for comment in posts_comments])
    posts_reactions = get_posts_reactions(access_token, posts_ids)
    reactions_users_ids = set([reaction['id'] for reaction in posts_reactions])
    reactions_statistic = {
        user_id: get_user_reactions_statistic(
            user_id, 
            posts_reactions, 
            facebook_reactions
        ) for user_id in reactions_users_ids}
    return commentators_ids, reactions_statistic
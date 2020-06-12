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


def determine_group_id(groups, group_title):
    for group in groups:
        group_name = group['name']
        if not group_name==group_title:
            continue
        group_id = group['id']
        return group_id


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


def get_commentators_ids(comments):
    comments_users_ids = []
    for comment in comments:
        user_id = comment['from']['id']
        comments_users_ids.append(user_id)
    return set(comments_users_ids)


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


def get_reactions_users_ids(reactions):
    reactions_users_ids = []
    for reaction in reactions:
        user_id = reaction['id']
        reactions_users_ids.append(user_id)
    return set(reactions_users_ids)


def get_user_reactions(reactions, user):
    user_reactions = []
    for reaction in reactions:
        user_id = reaction['id']
        if not user_id==user:
            continue
        reaction_type = reaction['type']
        user_reactions.append(reaction_type)
    return user_reactions


def get_user_reactions_statistic(user_id, reactions, facebook_reactions):
    user_reactions_statistic = {}
    for reaction in facebook_reactions:
        user_reactions = get_user_reactions(reactions, user_id)
        reactions_count = user_reactions.count(reaction)
        user_reactions_statistic[reaction] = reactions_count
    return user_reactions_statistic


def get_users_reactions_statistic(users_ids, reactions, facebook_reactions):
    users_reactions_statistic = {}
    for user_id in users_ids:
        user_reactions_statistic = get_user_reactions_statistic(user_id, reactions, facebook_reactions)
        users_reactions_statistic[user_id] = user_reactions_statistic
    return users_reactions_statistic


def fetch_facebook_analyze(access_token, user_id, days_count, months_count, facebook_reactions, group_name):
    groups = get_groups(access_token, user_id)
    group_id = determine_group_id(groups, group_name)

    if not group_id:
        exit(f'Группа {group_title} не найдена')

    group_posts = get_group_posts(access_token, group_id)
    posts_ids = [post['id'] for post in group_posts]
    start_date = calculate_start_date(days_count, months_count)
    posts_comments = get_posts_comments(
        access_token, 
        posts_ids, 
        start_date,
        )
    commentators_ids = get_commentators_ids(posts_comments)
    posts_reactions = get_posts_reactions(access_token, posts_ids)
    reactions_users_ids = get_reactions_users_ids(posts_reactions)
    users_reactions_statistic = get_users_reactions_statistic(
        reactions_users_ids, 
        posts_reactions, 
        facebook_reactions,
        )
    return commentators_ids, users_reactions_statistic
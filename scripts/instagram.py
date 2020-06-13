import datetime
from instabot import Bot
from operator import itemgetter
from .start_date import calculate_start_date


def get_last_posts(bot, group_id, posts_count):
    posts = bot.get_total_user_medias(group_id)
    last_posts = posts[-posts_count:]
    return last_posts


def get_comments_users_ids(comments, start_date):
    post_comments_users_ids = []
    for comment in comments:
        timestamp = comment['created_at']
        comment_date = datetime.datetime.utcfromtimestamp(timestamp)
        if comment_date < start_date:
            continue
        user_id=comment['user_id']
        post_comments_users_ids.append(user_id)
    return post_comments_users_ids


def get_top_commentators(users_ids):
    commentators = []
    users_ids_set = set(users_ids)
    for user_id in users_ids_set:
        comments_count = users_ids.count(user_id)
        commentators.append((user_id, comments_count))
        top_commentators = sorted(commentators, key=itemgetter(1), reverse=True)
        top_commentators_dict = {user_id:comments_count for user_id, comments_count in top_commentators}
    return top_commentators_dict


def fetch_instagram_analyze(login, password, posts_count, days_count, months_count, group_name):
    bot = Bot()
    bot.login(username=login, password=password)
    group_id = bot.get_user_id_from_username(group_name)
    last_posts = get_last_posts(
        bot,
        group_id,
        posts_count,
        )
    start_date = calculate_start_date(days_count, months_count)
    commentators_ids = []
    posts_commentators_ids = []
    for post in last_posts:
        post_comments = bot.get_media_comments_all(post)[::-1]
        post_comments_users_ids = get_comments_users_ids(post_comments, start_date)
        commentators_ids.extend(post_comments_users_ids)
        post_commentators_ids_set = set(post_comments_users_ids)
        posts_commentators_ids.extend(post_commentators_ids_set)
    comments_top = get_top_commentators(commentators_ids)
    posts_top = get_top_commentators(posts_commentators_ids)
    print('Comments Top:', comments_top)
    print('Posts Top:', posts_top)
import argparse
import os
from dotenv import load_dotenv
from scripts.facebook import get_facebook_analyze
from scripts.instagram import get_instagram_analyze
from scripts.vk import get_vk_analyze


FACEBOOK_DAYS_COUNT = 0
FACEBOOK_MONTHS_COUNT = 1
FACEBOOK_REACTIONS = [
    'LIKE', 
    'LOVE', 
    'WOW', 
    'HAHA', 
    'SAD', 
    'ANGRY', 
    'THANKFUL',
]
INSTAGRAM_POSTS_COUNT = 5
INSTAGRAM_DAYS_COUNT = 0
INSTAGRAM_MONTHS_COUNT = 3
VK_VERSION = 5.107
VK_DAYS_COUNT = 14
VK_MONTHS_COUNT = 0


def create_parser():
    parser = argparse.ArgumentParser(description='Инструмент для SMM аналитики')
    parser.add_argument('-n', '--network_name', help='Название социальной сети', type=str)
    parser.add_argument('-g', '--group_name', help='Название группы', type=str)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.network_name:
        exit('Введите название социальной сети')

    if not args.group_name:
        exit('Введите название группы')

    load_dotenv()
    facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    facebook_user_id = os.getenv('FACEBOOK_USER_ID')
    instagram_login = os.getenv("INSTAGRAM_LOGIN")
    instagram_password = os.getenv("INSTAGRAM_PASSWORD")
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    group_name = args.group_name
    network_name = args.network_name

    if network_name=='instagram':
        instagram_comments_top, instagram_posts_top = get_instagram_analyze(
            instagram_login, 
            instagram_password, 
            INSTAGRAM_POSTS_COUNT,
            INSTAGRAM_DAYS_COUNT,
            INSTAGRAM_MONTHS_COUNT,
            group_name,
            )
        print('Comments Top:', instagram_comments_top)
        print('Posts Top:', instagram_posts_top)

    if network_name=='vk':
        vk_audience_core = get_vk_analyze(
            vk_access_token,
            VK_VERSION,
            VK_DAYS_COUNT,
            VK_MONTHS_COUNT,
            group_name,
            )
        print('Audience core:', vk_audience_core)

    if network_name=='facebook':
        facebook_commentators_ids, facebook_reactions_statistic = get_facebook_analyze(
            facebook_access_token, 
            facebook_user_id,
            FACEBOOK_DAYS_COUNT,
            FACEBOOK_MONTHS_COUNT,
            FACEBOOK_REACTIONS,
            group_name,
            )
        print('Commentators:', facebook_commentators_ids)
        print('Reactions statistic:', facebook_reactions_statistic)


if __name__ == '__main__':
    main()
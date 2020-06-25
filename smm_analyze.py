import argparse
import configargparse
import os
from dotenv import load_dotenv
from scripts.facebook import fetch_facebook_analyze
from scripts.instagram import fetch_instagram_analyze
from scripts.vk import fetch_vk_analyze


FACEBOOK_REACTIONS = [
    'LIKE', 
    'LOVE', 
    'WOW', 
    'HAHA', 
    'SAD', 
    'ANGRY', 
    'THANKFUL',
]
VK_VERSION = 5.107


def create_parser():
    parser = configargparse.ArgParser(default_config_files=['config.ini'])
    parser.add('-c', '--config_file', is_config_file=True, help='Путь к файлу конфигурации')
    parser.add('--facebook_group_name', required=True, help='Название группы Facebook', type=str)
    parser.add('--facebook_days_count', help='Количество дней для анализа Facebook', type=int, default=0)
    parser.add('--facebook_months_count', help='Количество месяцев для анализа Facebook', type=int, default=1)
    parser.add('--instagram_group_name', required=True, help='Название группы Instagram', type=str)
    parser.add('--instagram_posts_count', help='Количество постов Instagram', type=int, default=5)
    parser.add('--instagram_days_count', help='Количество дней для анализа Instagram', type=int, default=0)
    parser.add('--instagram_months_count', help='Количество месяцев для анализа Instagram', type=int, default=3)
    parser.add('--vk_group_name', required=True, help='Название группы VK', type=str)
    parser.add('--vk_days_count', help='Количество дней для анализа VK', type=int, default=14)
    parser.add('--vk_months_count', help='Количество месяцев для анализа VK', type=int, default=0)
    subparsers = parser.add_subparsers()
    facebook_parser = subparsers.add_parser('facebook')
    facebook_parser.set_defaults(function=run_facebook_analyze)
    instagram_parser = subparsers.add_parser('instagram')
    instagram_parser.set_defaults(function=run_instagram_analyze)
    vk_parser = subparsers.add_parser('vk')
    vk_parser.set_defaults(function=run_vk_analyze)
    return parser


def run_facebook_analyze(args, authentication_summary):
    facebook_access_token = authentication_summary['facebook_access_token']
    facebook_user_id = authentication_summary['facebook_user_id']
    commentators, reactions_statistic = fetch_facebook_analyze(
        facebook_access_token, 
        facebook_user_id,
        args.facebook_days_count,
        args.facebook_months_count,
        FACEBOOK_REACTIONS,
        args.facebook_group_name,
        )
    print('Commentators:', commentators)
    print('Reactions statistic:', reactions_statistic)


def run_instagram_analyze(args, authentication_summary):
    instagram_login = authentication_summary['instagram_login']
    instagram_password = authentication_summary['instagram_password']
    comments_top, posts_top = fetch_instagram_analyze(
        instagram_login, 
        instagram_password, 
        args.instagram_posts_count,
        args.instagram_days_count,
        args.instagram_months_count,
        args.instagram_group_name,
        )
    print('Comments Top:', comments_top)
    print('Posts Top:', posts_top)


def run_vk_analyze(args, authentication_summary):
    vk_access_token = authentication_summary['vk_access_token']
    audience_core = fetch_vk_analyze(
        vk_access_token,
        VK_VERSION,
        args.vk_days_count,
        args.vk_months_count,
        args.vk_group_name,
        )
    print('Audience core:', audience_core)


def main():
    parser = create_parser()
    args = parser.parse_args()

    load_dotenv()
    facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    facebook_user_id = os.getenv('FACEBOOK_USER_ID')
    instagram_login = os.getenv("INSTAGRAM_LOGIN")
    instagram_password = os.getenv("INSTAGRAM_PASSWORD")
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    authentication_summary ={
        'facebook_access_token':facebook_access_token,
        'facebook_user_id':facebook_user_id,
        'instagram_login':instagram_login,
        'instagram_password':instagram_password,
        'vk_access_token':vk_access_token,
    }

    args.function(args, authentication_summary)


if __name__ == '__main__':
    main()
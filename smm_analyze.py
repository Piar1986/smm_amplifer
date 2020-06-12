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
    parser.add('-n', '--network_name', help='Название социальной сети', type=str)
    parser.add('-g', '--group_name', help='Название группы', type=str)
    parser.add('--facebook_days_count', required=True, help='Количество дней для анализа Facebook', type=int)
    parser.add('--facebook_months_count', required=True, help='Количество месяцев для анализа Facebook', type=int)
    parser.add('--instagram_posts_count', required=True, help='Количество постов Instagram', type=int)
    parser.add('--instagram_days_count', required=True, help='Количество дней для анализа Instagram', type=int)
    parser.add('--instagram_months_count', required=True, help='Количество месяцев для анализа Instagram', type=int)
    parser.add('--vk_days_count', required=True, help='Количество дней для анализа VK', type=int)
    parser.add('--vk_months_count', required=True, help='Количество месяцев для анализа VK', type=int)
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
        instagram_comments_top, instagram_posts_top = fetch_instagram_analyze(
            instagram_login, 
            instagram_password, 
            args.instagram_posts_count,
            args.instagram_days_count,
            args.instagram_months_count,
            group_name,
            )
        print('Comments Top:', instagram_comments_top)
        print('Posts Top:', instagram_posts_top)

    if network_name=='vk':
        vk_audience_core = fetch_vk_analyze(
            vk_access_token,
            VK_VERSION,
            args.vk_days_count,
            args.vk_months_count,
            group_name,
            )
        print('Audience core:', vk_audience_core)

    if network_name=='facebook':
        facebook_commentators_ids, facebook_reactions_statistic = fetch_facebook_analyze(
            facebook_access_token, 
            facebook_user_id,
            args.facebook_days_count,
            args.facebook_months_count,
            FACEBOOK_REACTIONS,
            group_name,
            )
        print('Commentators:', facebook_commentators_ids)
        print('Reactions statistic:', facebook_reactions_statistic)


if __name__ == '__main__':
    main()
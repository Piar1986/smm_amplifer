# Амплифер. Инструмент для SMM аналитики социальных сетей: Facebook, Instagram, VK (ВКонтакте)

#### Instagram
Исследование группы Instagram. 

Вывод в терминал рейтингов:
1. Общее количество комментариев по аккаунтам;
2. Число откомментированных аккаунтом постов.

#### ВКонтакте
Вывод в терминал ядра аудитории - список ID аккаунтов пользователей. Условия: откомментировать и лайкнуть один из постов.

#### Facebook 
Facebook запретил исследовать чужие группы. Доступно исследование только собственной группы.

Вывод в терминал:
1. Список аккаунтов комментаторов;
2. Статистика по эмоциям.

Исходные данные для анализа содержатся в файле конфигурации `config.ini`. Перед запуском скрипта укажите Ваши данные в файле.

### Как установить

Для использования скрипта необходимо:

1. Создать приложение  [ВКонтакте](https://vk.com/). Создать приложение можно в разделе [Мои приложения](https://vk.com/apps?act=manage). В качестве типа приложения следует указать `standalone` — это подходящий тип для приложений, которые просто запускаются на компьютере.
2. Получите сервисный ключ доступа `access token` в настройках Вашего приложения [ВКонтакте](https://vk.com/). Сервисный ключ доступа идентифицирует Ваше приложение. Все запросы к API, совершённые с использованием Вашего ключа доступа, будут считаться совершёнными от имени Вашего приложения.
3. Для работы с Facebook API нужен ключ доступа `access token` (маркер доступа пользователя). Получите ключ с правами `groups_access_member_info, manage_pages, pages_show_list, publish_pages, publish_to_groups` - [инструкция](https://developers.facebook.com/docs/graph-api/explorer/). Продлите [ключ доступа с 2-х часов до 2-х месяцев](https://developers.facebook.com/tools/debug/accesstoken/).

Скрипт берет часть данных из переменных окружения. Чтобы их определить создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следующие переменные:
- `FACEBOOK_USER_ID` - ID аккаунта пользователя [Facebook](https://www.facebook.com/)
- `FACEBOOK_ACCESS_TOKEN` - ключ доступа [Facebook](https://www.facebook.com/)
- `INSTAGRAM_LOGIN` — логин [Instagram](https://www.instagram.com/) аккаунта
- `INSTAGRAM_PASSWORD` — пароль от [Instagram](https://www.instagram.com/) аккаунта
- `VK_ACCESS_TOKEN` - ключ доступа [ВКонтакте](https://vk.com/)


Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Исходные данные

Перед запуском скрипта необходимо внеcите данные в файл конфигурации `config.ini`. Файл располагается рядом с `manage.py`. Формат данных: `ПЕРЕМЕННАЯ=значение`

Доступны следующие переменные:
- `facebook_group_name` - название группы Facebook;
- `facebook_days_count` - количество дней для анализа Facebook;
- `facebook_months_count` - количество месяцев для анализа Facebook;
- `instagram_group_name` - название группы Instagram;
- `instagram_posts_count` - количество постов Instagram;
- `instagram_days_count` количество дней для анализа Instagram;
- `instagram_months_count` - количество месяцев для анализа Instagram;
- `vk_group_name` - название группы VK;
- `vk_days_count` количество дней для анализа VK;
- `vk_months_count` - количество месяцев для анализа VK.

Значения по умолчанию:
```
facebook_days_count=0
facebook_months_count=1
instagram_posts_count=5
instagram_days_count=0
instagram_months_count=3
vk_days_count=14
vk_months_count=0
```

Файл конфигурации содержит разделы: `[facebook], [instagram], [vk]`. Укажите значение переменной в соответствующий раздел.

Пример минимального набора настроек, необходимых для запуска:
```
[facebook]
facebook_group_name=smm_analyze
[instagram]
instagram_group_name=cocacolarus
[vk]
vk_group_name=cocacola
```

### Как запустить

Пример команды запуска:
```
python smm_analyze.py instagram
```

Пример результата для VK и Facebook:

![](result_example.png)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
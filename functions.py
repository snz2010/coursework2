import json


def get_all_posts(path):
    """
    поиск всех постов из файла постов
    :return: данные из файла json
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_post_by_user(username, path):
    """
    поиск постов определенного пользователя
    :param username: интересующий нас пользователь
    :return: список постов пользователя
    """
    posts = get_all_posts(path)
    user_posts = []
    for post in posts:
        if username == post["poster_name"]:
            user_posts.append(post)
    return user_posts


def search_for_posts(ask, path):
    """
    поиск постов, содержащих слово/фразу
    :param ask: слово/фраза
    :return: список постов с искомой фразой
    """
    posts = get_all_posts(path)
    asked_posts = []
    ask = ask.lower()
    for post in posts:
        if ask in post["content"].lower():
            asked_posts.append(post)
    return asked_posts


def get_post_by_pk(pk, path):
    """
    поиск поста по идентификатору
    :param pk: идентификатор
    :return: 1 запись из файла
    """
    posts = get_all_posts(path)
    for post in posts:
        if pk == post["pk"]:
            return post


def get_all_comments(path):
    """
    чтение всех комментариев из файла
    :param path: путь к файлу комментариев
    :return: список словарей комментариев
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# запись новых комментариев
def write_all_comments(path, data):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def get_comments_by_post_pk(pk, path):
    """
    чтение списка комментариев к посту
    :param pk: идентификатор поста, к которому сделан комментарий
    :param path: путь к файлу с комментариями
    :return: список словарей
    """
    if pk < 1:
        return []
    comments = get_all_comments(path)
    list = []
    for comment in comments:
        if pk == comment["post_id"]:
            list.append(comment)
    return list


def get_posts_by_tag(tag, path):
    """
    чтение списка постов по тегу
    :param tag: параметр поиска
    :param path: путь к файлу с постами
    :return: список словарей
    """
    if pk < 1:
        return []
    comments = get_all_comments(path)
    list = []
    for comment in comments:
        if pk == comment["post_id"]:
            list.append(comment)
    return list


# формирование тега внутри контента в виде гиперссылки
def make_tag_link(raw_content, start):
    # ищем в контенте "#"
    start_n = raw_content.find("#", start)
    if start_n == -1:
        return raw_content  # вернем исходный, если "#" не найден
    # формируем тег ссылки
    stop_n = raw_content.find(" ", start_n + 2)
    tag = raw_content[start_n + 1:stop_n]
    # формируем новый контент с гиперссылкой
    content = (raw_content[0:start_n] +
               '<a href="/tag/' + tag + '">#' + tag + '</a>' +
               raw_content[stop_n:])
    return content


# считаем из json-файла текущие закладки
def read_bookmarks(path):
    with open(path, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    return current_data


# пишем в файл json новые закладки
def write_bookmarks(path, new_data):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False)

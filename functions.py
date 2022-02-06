import re


def search_tags(data):
    """
    наполнение выпадающего списка тегами
    :param data: словарь из файла
    :return: список найденных тэгов
    """
    tag_pattern = "#\S+"
    all_tags = []
    for item in data:
        tek_tags = re.findall(tag_pattern, item["content"])
        for tag in tek_tags:
            if tag not in all_tags:
                all_tags.append(tag)
    out_list = []
    # уберем символ # из строки тега
    for tag in all_tags:
        tag = tag.replace('#', '')
        out_list.append(tag)
    return out_list


def search_selected_tags(data, tag):
    """
    поиск списка тегов, подходящих по искомому
    :param data: словарь из файла
           tag: искомый тег
    :return: список найденных тэгов
    """
    selected_tags = []
    for item in data:
        if tag in item["content"]:
            selected_tags.append(item)
    return selected_tags

import os
from pathlib import Path
from flask import Flask, request, render_template, redirect
from functions import get_all_posts, get_comments_by_post_pk, get_post_by_user, get_post_by_pk, search_for_posts, \
    make_tag_link, read_bookmarks, write_bookmarks, get_all_comments, write_all_comments

POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOK_PATH = "data/bookmarks.json"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# обработчик главной страницы: ЛЕНТА ПОСТОВ
@app.route("/")
def page_index():
    posts = get_all_posts(POST_PATH)
    bookmarks = read_bookmarks(BOOK_PATH)
    # реализуем укороченную версию контента - через срез 50 символов
    for post in posts:
        post["content"] = post["content"][0:46] + "..."
        post["content"] = make_tag_link(post["content"], 0)
    return render_template("index.html", posts=posts, bookmarks_count=len(bookmarks), bookmarks=bookmarks)


# обработчик подробной странички поста - с комментариями и полным текстом
@app.route("/posts/<int:post_pk>")
def page_single_post(post_pk):
    # выбор поста по идентификатору
    post = get_post_by_pk(post_pk, POST_PATH)
    # сбор комментариев к выбранному посту
    comments = get_comments_by_post_pk(post_pk, COMMENTS_PATH)
    # подсчет числа комментов
    number_of_comments = len(comments)
    return render_template("post.html", post=post, comments=comments, number_of_comments=number_of_comments)


# обработчик поиска по содержимому постов
@app.route("/search")
def page_search():
    # поисковая фраза
    query = request.args.get("s")
    if not query or query == "":
        return "Вы ничего не запросили ..."
    # подходящие запросу посты
    posts = search_for_posts(query, POST_PATH)
    for post in posts:
        post["content"] = make_tag_link(post["content"], 0)
    # их количество
    number_of_posts = len(posts)
    return render_template("search.html", posts=posts, number_of_posts=number_of_posts, query=query)


# обработчик вывода постов конкретного пользователя
@app.route("/users/<username>")
def page_by_user(username):
    posts = get_post_by_user(username, POST_PATH)
    number_of_posts = len(posts)
    return render_template("user-feed.html", username=username, posts=posts, number_of_posts=number_of_posts)


# обработчик перехода по тегу
@app.route("/tag/<tag_name>")
def page_tag(tag_name):
    # получим искомый тег
    if len(tag_name) < 1:
        return "Ошибочка: Отсутствует тег поиска!"
    # подходящие запросу посты
    posts = search_for_posts("#" + tag_name, POST_PATH)
    for post in posts:
        post["content"] = make_tag_link(post["content"], 0)
    return render_template("tag.html", posts=posts, tag_name=tag_name)


# обработчик добавления поста в закладки
@app.route("/add/<int:post_id>")
def page_add_bm(post_id):
    # получим текущие закладки
    bookmarks = read_bookmarks(BOOK_PATH)
    # добавим выбранный пост
    if post_id not in bookmarks:
        bookmarks.append(post_id)
    write_bookmarks(BOOK_PATH, bookmarks)
    return redirect("/", code=302)  # После добавления переадресуйте на главную страницу


# представление с удалением из закладок
@app.route("/del/<int:post_id>")
def page_del_bm(post_id):
    # получим текущие закладки
    bookmarks = read_bookmarks(BOOK_PATH)
    # удалим переданную закладку
    bookmarks.remove(post_id)
    write_bookmarks(BOOK_PATH, bookmarks)
    return redirect("/", code=302)


# представление для вывода закладок
@app.route("/bookmarks/<int:bm_count>")
def page_bm(bm_count):
    if bm_count == 0:
        return redirect("/", code=302)
    if bm_count > 0:
        # получим текущие закладки
        bookmarks = read_bookmarks(BOOK_PATH)
        # прочитаем посты
        posts = []
        for item in bookmarks:
            posts.append(get_post_by_pk(item, POST_PATH))
        return render_template("bookmarks.html", posts=posts)


# представление для добавления комментария к посту
@app.route("/add_comment")
def page_add_comment():
    # получим данные из формы
    commenter_name = request.args.get("commenter_name")
    comment = request.args.get("comment")
    post_id = request.args.get("post_id")
    print(f"\n c_n={commenter_name}; comm={comment}; post_id={post_id}\n")
    # чтение файла комментариев
    comments = get_all_comments(COMMENTS_PATH)
    # формирование нового
    new_comment = {}
    new_comment["post_id"] = int(post_id)
    new_comment["commenter_name"] = commenter_name
    new_comment["comment"] = comment
    new_comment["pk"] = int(comments[len(comments)-1]["pk"]+1)
    comments.append(new_comment)
    # запись в файл всех комментариев
    write_all_comments(COMMENTS_PATH, comments)
    return redirect("/", code=302)

os.chdir(Path(os.path.abspath(__file__)).parent)
app.run()

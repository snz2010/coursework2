import os
from pathlib import Path
from flask import Flask, request, render_template, send_from_directory, redirect
import json
from functions import search_tags, search_selected_tags

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def page_index():
    # считываем из файла теги
    with open(POST_PATH, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    # ищем теги среди считанного
    all_tags = search_tags(current_data)
    # выводим найденные теги в выпадающем списке
    return render_template("index.html", all_tags=all_tags)


@app.route("/tag", methods=["GET", "POST"])
def page_tag():
    if request.method == "POST":
        # получим искомый тег
        selected_tag = request.form.get("tag")
        if selected_tag is None:
            return "<h1>Ошибочка: Отсутствует тег поиска!</h1>"
        # считываем из файла теги
        with open(POST_PATH, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        # выберем содержащие этот тег записи
        selected_tags = search_selected_tags(current_data, selected_tag)
        return render_template("post_by_tag.html", selected_tags=selected_tags, selected_tag=selected_tag)
    else:
        return f"<h1>Тег поиска - задан через GET</h1>"


@app.route("/post", methods=["GET"])
def page_post_create():
    return render_template("post_form.html")


@app.route("/post", methods=["POST"])
def new_post_create():
    # получим новые данные
    picture = request.files.get("picture")
    content = request.form.get("content")
    # редирект обратно, если файл-картинка не пришел
    if not picture:
        return redirect("/post")
    filename = picture.filename
    # сформируем путь к файлу с картинкой для её записи в разрешённый каталог
    path = "./" + UPLOAD_FOLDER + "/" + filename
    picture.save(path)  # сохраним картинку
    # сформируем ссылку для сервера и записи её в файл json
    picture_url = "/" + UPLOAD_FOLDER + "/" + filename
    # считаем из json-файла текущий словарик тегов
    with open(POST_PATH, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    # пишем в файл json новые данные
    with open(POST_PATH, "w", encoding='utf-8') as f:
        current_data.append({"pic": picture_url, "content": content})
        json.dump(current_data, f, ensure_ascii=False)
    return render_template("post_uploaded.html", picture=picture_url, content=content)


# ВАЖНАЯ ФУНКЦИЯ, БЕЗ КОТОРОЙ НЕ ОТОБРАЖАЮТСЯ ФАЙЛЫ КАРТИНОК ИЗ /uploads
@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


os.chdir(Path(os.path.abspath(__file__)).parent)
app.run()

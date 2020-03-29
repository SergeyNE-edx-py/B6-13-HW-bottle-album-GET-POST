# 1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит на экран сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов
# 2. Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем данные об альбоме. Данные передаются в формате веб-формы. 
#    Если пользователь пытается передать данные об альбоме, который уже есть в базе данных, обработчик запроса отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение
# 3. Набор полей в передаваемых данных полностью соответствует схеме таблицы album базы данных.
# 4. В качестве исходной базы данных использовать файл albums.sqlite3.
# 5. До попытки сохранить переданные пользователем данные, нужно провалидировать их. Проверить, например, что в поле "год выпуска" передан действительно год.

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from bottle import HTTPResponse

import sqlalchemy_album as album

# примеры GET запроса: 
# http -f GET localhost:8080/albums/Pink%20Floyd
# http -f GET localhost:8080/albums/Beatles
# http -f GET localhost:8080/albums/Beatles%20New
@route("/albums/<artist>")
def findalbum(artist):
    session = album.connect_db()
    albums_list = album.find(session, artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Найдено {} альбомов {}<br>".format(len(album_names), artist)
        result += "<br>".join(album_names)

    session.close()

    return result

# примеры POST запросов:
# http -f POST localhost:8080/addalbum year="1966" artist="Beatles" genre="Rock and roll" album="Revolver" - существующий
# http -f POST localhost:8080/addalbum year="2016" artist="New Beatles" genre="Re Make" album="Para Bellum" - новый
@route("/albums/", method="POST")
def addalbum():
    session = album.connect_db()
    try:
        albumPOSTed = album.Album(
            year=int(request.forms.get("year")),
            artist=request.forms.get("artist"),
            genre=request.forms.get("genre"),
            album=request.forms.get("album")
        )
    except ValueError as err:
        message = "Недопустимые параметры: " + str(err)
        result = HTTPResponse(status=400, body=message)
        session.close()
        return result
    else:
        if albumPOSTed.year < 1940 or albumPOSTed.year > 2020:
            message = "Недопустимый год выхода альбома: " + str(albumPOSTed.year)
            result = HTTPResponse(status=400, body=message)
            session.close()
            return result

    albumFinded = album.find(session, albumPOSTed.artist, albumPOSTed.album)
    if albumFinded:
        message = "Такой альбом уже есть: {}, {}, {}, {}".format(albumFinded.year, albumFinded.artist, albumFinded.genre, albumFinded.album)
        result = HTTPResponse(status=409, body=message)
    else: 
        album.add(session, albumPOSTed)
        message = "Добавлен альбом: {}, {}, {}, {}".format(albumPOSTed.year, albumPOSTed.artist, albumPOSTed.genre, albumPOSTed.album)
        result = message

    session.close()

    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=False)

B6-13-HW-bottle-album-GET-POST
B6.13 HW Сервер на bottle БД album, запросы GET, POST

Задание:

1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит на экран сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов.
2. Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем данные об альбоме. Данные передаются в формате веб-формы. Если пользователь пытается передать данные об альбоме, который уже есть в базе данных, обработчик запроса отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.
3. Набор полей в передаваемых данных полностью соответствует схеме таблицы album базы данных.

4. В качестве исходной базы данных использовать файл albums.sqlite3.

5. До попытки сохранить переданные пользователем данные, нужно провалидировать их. Проверить, например, что в поле "год выпуска" передан действительно год.

БД albums.sqlite3 можно скачать здесь: https://drive.google.com/open?id=1KHKrio-StI9jVIVgJH1EKaObpAFzRx25 

примеры GET запросов:

http -f GET localhost:8080/albums/Pink%20Floyd

http -f GET localhost:8080/albums/Beatles

http -f GET localhost:8080/albums/Beatles%20New


примеры POST запросов:

http -f POST localhost:8080/addalbum year="1966" artist="Beatles" genre="Rock and roll" album="Revolver" - существующий альбом

http -f POST localhost:8080/addalbum year="2016" artist="New Beatles" genre="Re Make" album="Para Bellum" - новый альбом


!Внимание: если одновременно использовать утилиту http и браузер (для GET запросов - http://localhost:8080/albums/Beatles) - возникает конфликт (и "залипание" http утилиты) из-за однопоточности bottle.

см. https://sf-python-fullstack.slack.com/archives/CMSJC3DT6/p1585474931011500

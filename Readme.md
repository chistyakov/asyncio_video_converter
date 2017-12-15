# Task from job interview

Разработать сервис, взаимодействующий с клиентами по REST API  и реализующий следующие методы:

1. Метод осуществляющий создание задачи на конвертацию медиа файла в HLS c помощью ffmpeg (параметры кодирования, количество профилей произвольные). Исходные медиа файлы расположены на файловой системе сервера.
2. Метод осуществляющий проверку статуса выполнения задачи, например по присвоенному идентификатору или адресу исходного медиа-файла на файловой системе.
3. Метод осуществляющий получение результата выполнения задачи. В ответе должна присутствовать доступная для проигрывания http-ссылка.

## How to run
```shell
docker build . -t converter2hls
docker run -d -p 8080:8080 --name converter2hls -v ${PWD}/input:/input converter2hls
Ctrl+C
```
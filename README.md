# Dating-service

## Как запустить 

1) Клонируйте репозитоий 
```bash
git clone git@github.com:inmedvedev/dating-service.git
```
2) Перейдите в директорию dating-service
```bash
cd dating-service
```
3) Скопируйе .env файл (прислал HR'у)

4)Соберите контейнеры и запустите
```bash
docker compose up --build -d
```
5) Запустить миграцию
```bash
docker exec -it dating-service-backend-1 python manage.py migrate
```
Сервис будет доступен по адресу http://0.0.0.0:8000/

## Импортировать тестовые данные в бд 

```bash
docker exec -it dating-service-backend-1 python manage.py export_participants -p participants.jsonl
```

## Описание эндпоинтов

- /api/send_confirmation-code/ - отправка email'a, для которого требуется подтверждение
- /api/login/ - логин, требуется ввод email и кода подтверждения, пришедшего на почту (сейчас сообщение пишется в консоль, smpt сервер настроен, нужно лишь поменять параметр EMAIL_BACKEND на  'django.core.mail.backends.smtp.EmailBackend') 
- /api/preferences/ - получение и создание предпочтнеий для конкретного пользователя
- /api/preferences/delete/{название предпочтения} - удаление предпочтения для конкретного пользователя
- /api/rating/ - создать рейтинг наиболее совместимых участников, выполняется в Celery


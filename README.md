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
4) Запустить миграцию
```bash
docker exec -it dating-service-backend-1 python manage.py migrate
```
Сервис будет доступен по адресу http://0.0.0.0:8000/

## Импортировать тестовые данные в бд 

```bash
docker exec -it dating-service-backend-1 python manage.py export_participants -p participants.jsonl
```



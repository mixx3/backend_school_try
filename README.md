# File backend
Бэкенд файлового хранилища

## Запуск
* Подключение к серверу по ssh `ssh ubuntu@10.22.1.105`
* Docker на сервере уже есть, нужно только дать доступ к docker deamon для пользователя:
`sudo usermod -aG docker $USER && sudo chmod 666 /var/run/docker.sock`
### Поднимаем базу
* Запускаем контейнер с Postgresql в докере на сервере: `docker run --name yandex-pg-13.3 -p 5432:5432 -e POSTGRES_USER=parfenovma -e POSTGRES_PASSWORD=v3rystrongpa55wrd-e POSTGRES_DB=dev -d postgres:13.3`
### Поднимаем бэкенд
(я не devOps конечно, но по-моему так проекты лучше не поднимать)
* `git clone https://github.com/mixx3/backend_school_try.git`
* `docker build .`
* `docker run --expose 80 --restart always {backend_image_id}`

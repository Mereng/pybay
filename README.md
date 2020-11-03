# Кофигурация
Необходимо поместить файл с названием `settings.yaml` в директорию `pybay`

### Содержимое файла конфигурации

```yaml
db: # настройка подключения к базе данных
  host: 127.0.0.1
  port: 5432
  database: pybay
  user: user
  password: 123456
jwt: # настройка генерации JWT-токенов
  secret: '123456'
  algorithm: 'HS256'
smtp: # настройка подключения SMTP для отправки почты
  host: 'smtp.yandex.ru'
  ssl: true
  login: 'login'
  from: 'from'
  password: 'password'
```

# Запуск
Приложение запускается путем запуска скрипта `app.py`.
```shell script
$ python pybay/app.py
```
Отдельно есть CLI-worker `cli.py` для проверок окончаний аукционов.

Запуск:
```shell script
$ python pybay/cli.py run_check_end_auctions
```

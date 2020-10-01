<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple REST API with Python running on AWS Lambda and API Gateway using the Serverless Framework v1.'
layout: Doc
framework: v1
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->
# Kanban-board

## Serverless Framework Python REST API on AWS


### API

**Корень сайта. Возвращает сообщение с приветствием:**

метод: **GET**

URL: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/

**Получить список задач:**

метод: **GET**

URL: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/tasks

**Создать задачу:**

метод: **POST**

URL: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/tasks

Content-Type: application/json

тело запроса: { "title": "some task title" }

**Обновить статус задачи:**

метод: **PATCH**

URL: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/tasks/{id}

Content-Type: application/json

тело запроса: { "status": 1 }

0 - todo

1 - in progress

2 - done

### Настроийка

Запустите эту команду, чтобы инициализировать новый проект в новом рабочем каталоге.

`sls init aws-python-rest-api`

### Использование

**Развертывание**

Этот пример предназначен для работы с информационной панелью Serverless Framework, которая включает расширенные функции, такие как CI / CD, мониторинг, метрики и т.д.

```
$ serverless login
$ serverless deploy
```

Для развертывания без панели инструментов вам нужно будет удалить поля `org` и `app` из `serverless.yml`, и вам не нужно будет запускать `sls login` перед развертыванием.

**Вызов функции локально.**

```
serverless invoke local --function hello
```

**Вызвать функцию**

```
curl https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
```

**Запуск локально**

- В файле serverless.yml закомментировать строки:
```
  environment:
    host: database-1.c1wirqdqpjjf.eu-central-1.rds.amazonaws.com
    dbname: kanbanboardsls
    user: postgres
    pass: postgresrootpass
    port: 5432
```
- В файле serverless.yml раскомментировать строки:
```
plugins:
  - serverless-offline
```

- В корневой папке проекта выполнить команду:
```
serverless offline
```
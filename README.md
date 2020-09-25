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

### Setup

Run this command to initialize a new project in a new working directory.

`sls init aws-python-rest-api`

### Usage

**Deploy**

This example is made to work with the Serverless Framework dashboard which includes advanced features like CI/CD, monitoring, metrics, etc.

```
$ serverless login
$ serverless deploy
```

To deploy without the dashboard you will need to remove `org` and `app` fields from the `serverless.yml`, and you won’t have to run `sls login` before deploying.

**Invoke the function locally.**

```
serverless invoke local --function hello
```

**Invoke the function**

```
curl https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
```



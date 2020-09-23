import json
from services.kanbanBoardService import KanbanBoardService

# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
# type in console: aws configure
# Default region name [None]: us-east-1
# Default output format [None]: json

# Show configure list in console:
# aws configure list

# curl http://localhost:3000/
# {"currentRoute":"get - /","error":"Serverless-offline: route not found.","existingRoutes":["get - /dev"],"statusCode":404}
# curl http://localhost:3000/dev


def hello(event, context):
    body = {
        "input": event,
        "message": "Kanban-board!"
    }
    response = {
        "body": json.dumps(body),
        "status_code": 200
    }
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


# Get tasks.
def get(event, context):
    service = KanbanBoardService()
    result = service.get_tasks(event)
    response = {
        "body": json.dumps(result['data']),
        "statusCode": result['status']
    }
    return response


def post(event, context):
    id = event.pathParameters.customerId

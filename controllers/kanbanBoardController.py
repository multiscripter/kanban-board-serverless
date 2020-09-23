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

# To run serverless-offline, type in the console:
# serverless offline


def hello(event, context):
    """Handles requests to root."""

    result = {
        'data': {
            'message': 'Kanban-board!'
        },
        'status': 200
    }
    return _get_response(result)

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def create(event, context):
    """Create task."""

    service = KanbanBoardService()
    result = service.create_task(event)
    return _get_response(result)


def get(event, context):
    """Get tasks."""

    service = KanbanBoardService()
    result = service.get_tasks(event)
    return _get_response(result)


def update(event, context):
    """Update task."""

    service = KanbanBoardService()
    result = service.update_task(event)
    return _get_response(result)


def _get_response(result):
    response = {
        "body": json.dumps(result['data']),
        "statusCode": result['status']
    }
    return response

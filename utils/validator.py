import json


class Validator:

    def __init__(self):
        self.body = dict()
        self.errors = dict()

    def validate(self, event, result, fields):
        if event is None:
            raise Exception('Parameter "event" is None')
        if result is None:
            raise Exception('Parameter "result" is None')
        if fields is None:
            raise Exception('Parameter "fields" is None')

        if event['body'] is None:
            self.errors['body'] = 'body is not set'
            result['status'] = 400  # Bad Request.

        if not self.errors:
            self.body = json.loads(event['body'])
            if not bool(self.body):
                self.errors['body'] = 'body is empty'
                result['status'] = 400  # Bad Request.

        if not self.errors:
            for field, checks in fields.items():
                for check in checks:
                    if field not in self.errors and check == 'is_set':
                        self.is_set(field)
                    if field not in self.errors and check == 'is_empty':
                        self.is_empty(field)

        if self.errors:
            result['status'] = 400  # Bad Request.
        else:
            event['body'] = self.body
        return self.errors

    def is_set(self, field):
        if field not in self.body:
            self.errors[field] = field + ' is not set'
        elif isinstance(self.body[field], str):
            self.body[field] = self.body[field].strip()

    def is_empty(self, field):
        if not isinstance(self.body[field], (int, float)) and not self.body[field]:
            self.errors[field] = field + ' is empty'

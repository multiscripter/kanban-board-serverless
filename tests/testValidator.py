import unittest
from utils.validator import Validator

# Запуск тестов из корня проекта с генерацией покрытия кода.
# coverage erase
# coverage run -m pytest -p no:cacheprovider ./tests/*.py
# coverage html

# coverage не покрывает файлы в корне проекта (kanbanBoardController.py)


class TestValidator(unittest.TestCase):
    """Test Validator."""

    def test_validate_event_is_none(self):
        """Test: validate(self, event, result, fields)
        Exception: Parameter "event" is None."""

        validator = Validator()
        with self.assertRaises(Exception) as ctx_mng:
            validator.validate(None, {}, {})
        ex = ctx_mng.exception
        self.assertEqual('Parameter "event" is None', str(ex))

    def test_validate_result_is_none(self):
        """Test: validate(self, event, result, fields)
        Exception: Parameter "result" is None."""

        validator = Validator()
        with self.assertRaises(Exception) as ctx_mng:
            validator.validate({}, None, {})
        ex = ctx_mng.exception
        self.assertEqual('Parameter "result" is None', str(ex))

    def test_validate_fields_is_none(self):
        """Test: validate(self, event, result, fields)
        Exception: Parameter "fields" is None."""

        validator = Validator()
        with self.assertRaises(Exception) as ctx_mng:
            validator.validate({}, {}, None)
        ex = ctx_mng.exception
        self.assertEqual('Parameter "fields" is None', str(ex))

    def test_validate_body_is_none(self):
        """Test: validate(self, event, result, fields)
        Error: body is not set."""

        event = {'body': None}
        validator = Validator()
        errors = validator.validate(event, {}, {})
        self.assertEqual('body is not set', errors['body'])

    def test_validate_body_is_empty(self):
        """Test: validate(self, event, result, fields)
        Error: body is empty."""

        event = {'body': "{}"}
        validator = Validator()
        errors = validator.validate(event, {}, {})
        self.assertEqual('body is empty', errors['body'])

    def test_validate_fields_is_not_set(self):
        """Test: validate(self, event, result, fields)
        Error: field + ' is not set'"""

        event = {'body': '{"foo":"bar"}'}
        fields = {
            'title': ['is_set']
        }
        validator = Validator()
        errors = validator.validate(event, {}, fields)
        self.assertEqual('title is not set', errors['title'])

    def test_validate_fields_is_empty(self):
        """Test: validate(self, event, result, fields)
        Error: field + ' is empty'"""

        event = {'body': '{"title":""}'}
        fields = {
            'title': ['is_empty']
        }
        validator = Validator()
        errors = validator.validate(event, {}, fields)
        self.assertEqual('title is empty', errors['title'])

    def test_validate_fields_success(self):
        """Test: validate(self, event, result, fields)"""

        event = {'body': '{"title":"test-title"}'}
        fields = {
            'title': ['is_set', 'is_empty']
        }
        validator = Validator()
        errors = validator.validate(event, {}, fields)
        self.assertEqual({}, errors)

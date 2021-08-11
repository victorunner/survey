from django.core.exceptions import ValidationError


def validate_choices(value):
    if value and len(value) != len(set(value)):
        raise ValidationError('Choices should not be repeated.')


def validate_answers_pool(value):
    if value is not None and len(value) < 2:
        raise ValidationError('Answers pool should provide at least two questions.')

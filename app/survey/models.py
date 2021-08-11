from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from .validators import validate_answers_pool, validate_choices

User = get_user_model()


class Category(models.Model):
    # id создаем явно, чтобы была возможность задать help_text для документации
    id = models.AutoField(
        'ID категории',
        primary_key=True,
        help_text='ID категории'
    )
    name = models.CharField(
        'категория опроса',
        max_length=64,
        unique=True
    )
    slug = models.SlugField(
        'слаг опроса',
        max_length=32,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Question(models.Model):
    SINGLE_CHOICE_ANSWER = 'S'
    MULTIPLE_CHOICE_ANSWER = 'M'
    OPEN_ANSWER = 'O'
    ANSWER_TYPE_CHOICES = [
        (SINGLE_CHOICE_ANSWER, 'Единственный вариант ответа'),
        (MULTIPLE_CHOICE_ANSWER, 'Множественный вариант ответа'),
        (OPEN_ANSWER, 'Свободный ответ'),
    ]

    text = models.CharField(
        'текст вопроса',
        max_length=128
    )
    answer_type = models.CharField(
        'тип ответа на вопрос',
        max_length=1,
        choices=ANSWER_TYPE_CHOICES,
        default=OPEN_ANSWER
    )
    answers_pool = ArrayField(
        models.CharField(max_length=128),
        verbose_name='варианты ответов',
        blank=True,
        null=True,
        validators=[validate_answers_pool]
    )

    class Meta:
        ordering = ('answer_type', 'text',)

    def __str__(self):
        return f'Вопрос: {self.text[:32]}. Ответ: [тип {self.answer_type}].'


class Survey(models.Model):
    name = models.CharField(
        'имя опроса',
        max_length=64,
        unique=True
    )
    description = models.CharField(
        'описание опроса',
        max_length=128,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='surveys',
        blank=True,
        null=True
    )
    start_date = models.DateField(
        'дата начала опроса',
        editable=False
    )
    end_date = models.DateField(
        'дата конца опроса'
    )
    questions = models.ManyToManyField(
        Question,
        through='QuestionSurvey'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            now = timezone.now()
            self.start_date = now.date()
            # по умолчанию дается 2 недели на опрос
            self.end_date = (now + timezone.timedelta(weeks=2)).date()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('start_date', 'name')

    def __str__(self):
        return self.name


class QuestionSurvey(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question} {self.survey}'


class Answer(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='респондент',
        on_delete=models.CASCADE,
        related_name='answers',
        blank=True,
        null=True
    )
    survey = models.ForeignKey(
        Survey,
        verbose_name='опрос',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        Question,
        verbose_name='вопрос',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.TextField(
        'текст свободного ответа',
        blank=True
    )
    choices = ArrayField(
        models.PositiveSmallIntegerField(),
        blank=True,
        null=True,
        validators=[validate_choices]
    )
    anonym_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.question.question_type == Question.OPEN:
            return self.text
        return self.selected_answers

from collections import Counter

from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import AnswerFilter, SurveyFilter
from .models import Answer, Category, Question, Survey
from .permissions import AnswerPermission, IsAdminOrReadOnly
from .serializers import (AnswerSerializer, CategorySerializer,
                          QuestionSerializer, SurveyRetrieveListSerializer,
                          SurveySerializer)

anonym_id_filter_param = openapi.Parameter(
    'anonym_id',
    openapi.IN_QUERY,
    description=(
        'Фильтрация ответов по ID анонимных пользователей. ID присваивается сервером. '
        'Для общности, можно использовать ID `0`, означающее всех аутентиф-ых пользователей.'
    ),
    type=openapi.TYPE_INTEGER
)
user_filter_param = openapi.Parameter(
    'user',
    openapi.IN_QUERY,
    description=(
        'Фильтрация ответов по username пользователей. '
        'Для общности, можно использовать значение `anonym`, означающее всех анонимных пользователей.'
    ),
    type=openapi.TYPE_STRING
)
anonym_filter_param = openapi.Parameter(
    'anonym',
    openapi.IN_QUERY,
    description=(
        'Фильтрация ответов по 2 категориям: ответов, данных анонимными (если `1`/`true`) и '
        'аутентиф-ым пользователями (если `0`/`false`).'
    ),
    type=openapi.TYPE_BOOLEAN
)
active_filter_param = openapi.Parameter(
    'active',
    openapi.IN_QUERY,
    description=(
        'Фильтрация опросов по 2 категориям: опросов, активных (если `1`/`true`) и '
        'неактивных (если `0`/`false`) в настоящее время.'
    ),
    type=openapi.TYPE_BOOLEAN
)

# 201 Created
response_201_created = openapi.Response('Создание успешно.')
# 204 No Content
response_204_no_content = openapi.Response('Удаление успешно.')
# 400 Bad Request
response_400_bad_request = openapi.Response('Ошибка.')
# 401 Unauthorized
response_401_unauth = openapi.Response('JWT токен отсутствует/невалидный/истекший.')
# 403 Forbidden
response_403_forbidden = openapi.Response('Нет права доступа.')


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description=(
            'Создать категорию опроса.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            201: 'Категория успешно создана.',
            400: response_400_bad_request,
            401: response_401_unauth,
            403: response_403_forbidden
        },
        tags=('CATEGORIES',)
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить категорию опроса по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Категория.',
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Категория не найдена.'
        },
        tags=('CATEGORIES',)
    )
)
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить список всех категорий опроса.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Список категорий с пагинацией.',
            401: response_401_unauth,
            403: response_403_forbidden
        },
        tags=('CATEGORIES',)
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_description=(
            'Удалить категорию опроса по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            204: response_204_no_content,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Категория не найдена.'
        },
        tags=('CATEGORIES',)
    )
)
class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description=(
            'Создать вопрос.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            201: 'Вопрос успешно создан.',
            400: response_400_bad_request,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос не найден (вопрос создан).'
        },
        tags=('QUESTIONS',)
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить вопрос по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Вопрос.',
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Вопрос (или опрос) не найден.'
        },
        tags=('QUESTIONS',)
    )
)
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить список всех вопросов.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Список вопросов с пагинацией.',
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос не найден.'
        },
        tags=('QUESTIONS',)
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_description=(
            'Частично обновить вопрос по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Вопрос.',
            400: response_400_bad_request,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Вопрос (или опрос) не найден.'
        },
        tags=('QUESTIONS',)
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_description=(
            'Удалить вопрос по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            204: response_204_no_content,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Вопрос (или опрос) не найден.'
        },
        tags=('QUESTIONS',)
    )
)
class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        if 'survey_id' in self.kwargs:
            survey = get_object_or_404(Survey, id=self.kwargs['survey_id'])
            return survey.questions.all()
        return Question.objects.all()

    def perform_create(self, serializer):
        question = serializer.save()

        if 'survey_id' in self.kwargs:
            survey = get_object_or_404(Survey, id=self.kwargs['survey_id'])
            survey.questions.add(question)
            survey.save()


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description=(
            'Создать опрос.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            201: 'Опрос успешно создан.',
            400: response_400_bad_request,
            401: response_401_unauth,
            403: response_403_forbidden
        },
        tags=('SURVEYS',)
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить опрос по ID.\n\n'
            'Права доступа: **Доступно анонимным пользователям**.'
        ),
        responses={
            200: 'Опрос.',
            404: 'Опрос не найден.'
        },
        tags=('SURVEYS',)
    )
)
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить список всех опросов.\n\n'
            'Права доступа: **Доступно анонимным пользователям**.'
        ),
        responses={
            200: 'Список опросов с пагинацией.'
        },
        tags=('SURVEYS',),
        manual_parameters=(
            active_filter_param,
        )
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_description=(
            'Частично обновить опрос по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Опрос.',
            400: response_400_bad_request,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос не найден.'
        },
        tags=('SURVEYS',)
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_description=(
            'Удалить опрос по ID.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            204: response_204_no_content,
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос не найден.'
        },
        tags=('SURVEYS',)
    )
)
class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SurveyFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return SurveyRetrieveListSerializer
        return SurveySerializer


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description=(
            'Создать ответ на вопрос опроса.\n\n'
            'Права доступа: **Доступно анонимным пользователям**.'
        ),
        responses={
            201: 'Ответ успешно создан.',
            400: response_400_bad_request,
            401: response_401_unauth,
            404: 'Опрос не найден.'
        },
        tags=('ANSWERS',)
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить ответ на вопрос опроса по id.\n\n'
            'Права доступа: **Автор ответа, админ**.'
        ),
        responses={
            200: 'Ответ.',
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос (ответ) не найден.'
        },
        tags=('ANSWERS',)
    )
)
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description=(
            'Получить список всех ответов на вопрос опроса.\n\n'
            'Права доступа: **Админ**.'
        ),
        responses={
            200: 'Список всех ответов с пагинацей.',
            401: response_401_unauth,
            403: response_403_forbidden,
            404: 'Опрос не найден.'
        },
        tags=('ANSWERS',),
        manual_parameters=(
            anonym_filter_param,
            user_filter_param,
            anonym_id_filter_param
        )
    )
)
class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnswerFilter
    permission_classes = (AnswerPermission,)

    def get_queryset(self):
        survey = get_object_or_404(Survey, id=self.kwargs.get('survey_id'))
        question = get_object_or_404(Question, id=self.kwargs.get('question_id'))
        return Answer.objects.filter(survey=survey, question=question)

    def get_serializer_context(self):
        question = get_object_or_404(Question, id=self.kwargs['question_id'])

        context = super().get_serializer_context()
        context.update({
            'answer_type': question.answer_type,
            'answers_pool_size': len(question.answers_pool) if question.answers_pool else 0
        })

        return context

    def perform_create(self, serializer):
        survey = get_object_or_404(Survey, id=self.kwargs['survey_id'])
        question = get_object_or_404(Question, id=self.kwargs['question_id'])

        is_auth = self.request.user.is_authenticated

        anonym_id = 0
        if not is_auth:
            if 'ANONYM_ID' in self.request.session:
                anonym_id = self.request.session['ANONYM_ID']
            else:
                if not Answer.objects.exists():
                    # значение 0 - для аутентифицированных пользователей
                    anonym_id = 1
                else:
                    anonym_id = Answer.objects.aggregate(Max('anonym_id'))['anonym_id__max']
                self.request.session['ANONYM_ID'] = anonym_id

        serializer.save(
            user=self.request.user if is_auth else None,
            survey=survey,
            question=question,
            anonym_id=anonym_id
        )

    @swagger_auto_schema(
        method='get',
        operation_description=(
            'Получить статистику по ответам.\n\n'
            'Права доступа: **Админ**.'
        ),
        tags=['ANSWERS'],
        manual_parameters=[
            anonym_filter_param,
            user_filter_param,
            anonym_id_filter_param
        ]
    )
    @action(detail=False, methods=['get'])
    def stat(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        answers_total_count = qs.count()

        choices_counter = Counter()
        for v in qs.values_list('choices'):
            choices_counter.update(v[0])

        text_answers_count = qs.filter(text__isnull=False).count()

        statistics = dict(choices_counter)
        statistics['answersTotalCount'] = answers_total_count
        statistics['textAnswersCount'] = text_answers_count

        return Response(statistics)

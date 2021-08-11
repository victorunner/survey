from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    'surveys',
    views.SurveyViewSet,
    basename='survey'
)
router_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='category'
)
router_v1.register(
    'questions',
    views.QuestionViewSet,
    basename='question'
)
router_v1.register(
    r'surveys/(?P<survey_id>\d+)/questions',
    views.QuestionViewSet,
    basename='question'
)
router_v1.register(
    r'surveys/(?P<survey_id>\d+)/questions/(?P<question_id>\d+)/answers',
    views.AnswerViewSet,
    basename='answer',
)

urlpatterns = [path('v1/', include(router_v1.urls))]

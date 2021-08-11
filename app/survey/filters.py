import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Answer, Survey

User = get_user_model()


class SurveyFilter(filters.FilterSet):
    active = filters.BooleanFilter(method='active_filter')

    def active_filter(self, queryset, name, value):
        NOW = datetime.date.today()
        if value:
            return queryset.filter(
                start_date__lte=NOW,
                end_date__gte=NOW
            )
        return queryset.filter(
            Q(start_date__gt=NOW)  # опрос еще не начался
            | Q(end_date__lt=NOW)  # опрос уже закончился
        )

    class Meta:
        model = Survey
        fields = ('active',)


class AnswerFilter(filters.FilterSet):
    user = filters.CharFilter(method='user_filter')
    anonym = filters.BooleanFilter(field_name='user', lookup_expr='isnull')

    def user_filter(self, queryset, name, value):
        if value == 'anonym':
            return queryset.filter(user=None)
        return queryset.filter(user__username=value)

    class Meta:
        model = Answer
        fields = ('anonym', 'user', 'anonym_id')

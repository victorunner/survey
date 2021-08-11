from rest_framework import serializers

from .models import Answer, Category, Question, Survey


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class QuestionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        answer_type = data['answer_type']
        answers_pool = data.get('answers_pool')

        if answer_type == Question.OPEN_ANSWER:
            if answers_pool:
                raise serializers.ValidationError('Wrong question (only question text should be provided).')
        else:
            if not answers_pool:
                raise serializers.ValidationError('Wrong question (answers not provided).')
        return data

    class Meta:
        model = Question
        fields = ('id', 'answer_type', 'text', 'answers_pool')


class SurveySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Survey
        fields = (
            'name', 'description', 'category',
            'end_date',
            'questions'
        )


class SurveyRetrieveListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = (
            'id', 'name', 'description', 'category',
            'start_date', 'end_date',
            'questions'
        )


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    survey = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Survey.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Question.objects.all()
    )

    def validate(self, data):
        answer_type = self.context['answer_type']
        answers_pool_size = self.context['answers_pool_size']

        text = data.get('text')
        choices = data.get('choices')

        if answer_type == Question.OPEN_ANSWER:
            if not text or choices:
                raise serializers.ValidationError('Wrong open answer.')
        elif answer_type == Question.SINGLE_CHOICE_ANSWER:
            if text or not choices or len(choices) != 1:
                raise serializers.ValidationError('Wrong single choice answer.')
        elif answer_type == Question.MULTIPLE_CHOICE_ANSWER:
            if (
                    text
                    or not choices
                    or min(choices) < 0
                    or max(choices) >= answers_pool_size
            ):
                raise serializers.ValidationError('Wrong multiple choice answer.')
        else:
            raise serializers.ValidationError('Wrong answer type.')

        return data

    class Meta:
        model = Answer
        fields = ('id', 'user', 'survey', 'question', 'text', 'choices', 'anonym_id')

from rest_framework import serializers
from .models import Question

    
class QuestionListSerializer(serializers.ModelSerializer):

    question = serializers.EmailField(source='question_text')
    
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'was_published_recently_m']


class QuestionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'pub_date', 'question_text']

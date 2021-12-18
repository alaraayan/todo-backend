from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Todo

#! USER SERIALIZERS
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'

class PopulatedTodoSerializer(TodoSerializer):
    owner = UserSerializer()
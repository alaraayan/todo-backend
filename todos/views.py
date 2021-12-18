from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer

class TodoListView(APIView):
    #!GET ALL TODOS
    def get(self, _request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        return Response(serializer.data)
    #! CREATE A NEW TODO
    def create(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class TodoDetailView(APIView):
    # def get_todo(self, pk):
    #     try:
    #         return Todo.objects.get(pk=pk)
    #     except Todo.DoesNotExist:
    #         raise NotFound()
    #! DELETE A TODO
    def delete(self, _request)
    #! EDIT A TODO
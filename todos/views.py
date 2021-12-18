from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer, PopulatedTodoSerializer

# GET ALL AND CREATE NEW
class TodoListView(APIView):
    #!GET ALL TODOS
    def get(self, _request):
        todos = Todo.objects.all()
        serializer = PopulatedTodoSerializer(todos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    #! CREATE A NEW TODO
    def post(self, request):
        request.data['owner'] = request.user.id
        new_todo = TodoSerializer(data=request.data)
        if new_todo.is_valid():
            new_todo.save()
            return Response(new_todo.data, status=status.HTTP_201_CREATED)
        return Response(new_todo.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class TodoDetailView(APIView):
    # ! GET A SINGLE TODO
    def get_todo(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound()
    def get(self, _request, pk):
        todo = self.get_todo(pk=pk)
        serialized_todo = PopulatedTodoSerializer(todo)
        return Response(serialized_todo.data, status=status.HTTP_200_OK)

    # ! DELETE A TODO
    def delete(self, _request, pk):
        todo_to_delete = self.get_todo(pk=pk)
        todo_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ! EDIT A TODO
    def put(self, request, pk):
        todo_to_update = self.get_todo(pk=pk)
        request.data['owner'] = request.user.id
        updated_todo = TodoSerializer(todo_to_update, data=request.data)
        if updated_todo.is_valid():
            updated_todo.save()
            return Response(updated_todo.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_todo.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
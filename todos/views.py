from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Todo
from .serializers import TodoSerializer, PopulatedTodoSerializer

#GET ALL AND CREATE NEW
class TodoListView(APIView):
    permission_classes = (IsAuthenticated, )
    #! CREATE A NEW TODO
    def post(self, request):
        
        new_todo = TodoSerializer(data=request.data)
        request.data['owner'] = request.user.id
        if new_todo.is_valid():
            new_todo.save()
            return Response(new_todo.data, status=status.HTTP_201_CREATED)
        return Response(new_todo.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    #!GET ALL TODOS
    def get(self, request):
        todos = Todo.objects.all()
        serialized_todos = PopulatedTodoSerializer(todos, many=True)
        def check_owner(todo_item):
            # print('🍇', todo_item, todo_item['owner']['id'])
            if todo_item['owner']['id'] == request.user.id:
                return True
            return False
        filtered_todos = list(filter(check_owner, serialized_todos.data))
        
        return Response(filtered_todos, status=status.HTTP_200_OK)
    

#SHOW, DELETE AND UPDATE ONE
class TodoDetailView(APIView):
    permission_classes = (IsAuthenticated, )
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
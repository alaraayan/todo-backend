from django.db import models

class Todo(models.Model):
    todo_item = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='todos',
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return f'Todo {self.id}: {self.todo_item}'
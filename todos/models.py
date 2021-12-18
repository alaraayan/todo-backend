from django.db import models

class Todo(models.Model):
    todo_item = models.CharField(max_length=100)
    is_Active = models.BooleanField(default=True)
    is_Done = models.BooleanField(default=False)

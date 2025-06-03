from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Page(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

class Question_and_Answer(models.Model):
    page = models.ForeignKey(Page, related_name='questions', on_delete=models.CASCADE)#  on_delete=models.CASCADE means that if the page is deleted, the question and answer will be deleted
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

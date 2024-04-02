from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomerUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('manager', 'manager'),
        ('admin', 'admin')
    )
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField('Description', max_length=600, default='', blank=True)
    Start_Date = models.DateField(default=datetime.now)
    username = models.CharField(max_length=15, unique=True)
    password = models.TextField(default="password")
    Employee_Number = models.AutoField(auto_created=True, unique=True, primary_key=True, )

    def __str__(self):
        return self.username


class Task(models.Model):
    Task_ID = models.AutoField(primary_key=True)
    Alias_Assigned = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    Progress = models.CharField(default="TODO", max_length=25)
    Title = models.TextField()
    Desc = models.TextField()

    def __str__(self):
        return self.Title


class Comment(models.Model):
    Comment_ID = models.AutoField(primary_key=True)
    Task_ID = models.ForeignKey(Task, on_delete=models.CASCADE)
    Alias_Written = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    Comment = models.TextField()

    def __str__(self):
        return self.Comment

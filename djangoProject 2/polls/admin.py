# @admin.register(UserFeedback)
# class UserFeedbackAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'created_at')
from django.contrib import admin

from polls.models import CustomerUser, Task, Comment

admin.site.register(CustomerUser)
admin.site.register(Task)
admin.site.register(Comment)
# @admin.register(CustomerUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'username', 'Start_Date', 'Employee_Number', 'password', 'status')

#
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('Task_ID', 'Progress', 'Title', 'Desc')
# admin.site.register(Question)

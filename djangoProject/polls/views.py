import json
import re

from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.models import Task, CustomerUser, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Desc', 'Alias_Assigned', 'Title', 'Progress']


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        try:
            user = CustomerUser.objects.get(username=username)
        except CustomerUser.DoesNotExist:
            raise forms.ValidationError("Username not found.")

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid password.")

        if not user.check_password(password):
            raise forms.ValidationError("Invalid password.")

        return self.cleaned_data


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("2")
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect to a success page or home page
            return redirect('polls:display')
            # Handle invalid login credentials
            # error_message = "Invalid username or password."

        else:
            print("3")
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f'Error in {field}: {error}')
    return render(request, 'polls/Login.html')


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        missing_fields = []
        # Check if any of the required fields are empty
        for field_name, field_value in cleaned_data.items():
            if not field_value:
                missing_fields.append(field_name)

            # Add errors for missing fields
        for field_name in missing_fields:
            self.add_error(field_name, "This field is required.")

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errorMessage = "Password must"

        # Check for minimum length
        if len(password) < 8:
            errorMessage += " be at least 8 characters long"
        # Check for at least one digit
        if not any(char.isdigit() for char in password):
            errorMessage += "contain at least one digit"
        # Check for at least one special character (non-alphanumeric)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errorMessage += " contain at least one special character '!@#$%^&*(),.?:{}|<>'"
        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            errorMessage += " contain at least one uppercase letter"
        if errorMessage != "Password must":
            raise forms.ValidationError(errorMessage)

        return make_password(password)


def create_comment_form(request, task_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.Alias_Written = request.user
            comment.Task_ID = Task.objects.get(Task_ID=task_id)
            comment.save()
            return redirect('polls:display')
        else:
            error_messages = form.errors.as_json()
            return JsonResponse({'error': error_messages}, status=400)
    task = Task.objects.get(Task_ID=task_id)
    return render(request, "polls/comment.html", {'task': task})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:display')
        else:
            # Handle validation errors
            error_messages = form.errors.as_json()
            return JsonResponse({'error': error_messages}, status=400)

    return JsonResponse({'error': 'Unsupported method'}, status=405)


def user_create(request):
    # errorMessage = ""
    print("1")
    if request.method == "POST":
        print("2")
        form = UserForm(request.POST)
        print("3")

        if form.is_valid():
            print("4")
            user = form.save(commit=False)

            print("5")
            user.password = form.cleaned_data['password']
            print("6")
            print(user)
            user.save()
            print("7")
            messages.success(request, 'Registration Successful')
            print("8")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    return render(request, 'polls/Login.html')
    # return render(request, "polls:Login")


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required()
def DisplayUsers(request):
    # if not request.user.is_authenticated:
    #     redirect('/')
    # Fetch all polls from the database
    tasks = Task.objects.all()
    return render(request, 'polls/display.html', {'Tasks': tasks})


@login_required
@csrf_exempt
def delete_task(request):
    if request.method == "POST":
        try:
            taskID = request.POST.get('taskID')
            taskToDelete = Task.objects.get(Task_ID=taskID)
            taskToDelete.delete()
            return redirect('polls:display')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Unsupported method'}, status=405)


@login_required
def create_new_task_form(request):
    users = CustomerUser.objects.all()

    return render(request, 'polls/new_task.html', {'users': users})


# def task_create(request):
#     # Alias_Assigned = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Progress = models.CharField(default="TODO", max_length=25)
#     # Title = models.TextField()
#     # Desc = models.TextField()
#     if request.method == "POST":
#         try:
#             title = request.POST.get('title')
#             desc = request.POST.get('desc')
#             progress = request.POST.get('progress')
#             assigned_to = request.POST.get('assigned')  # Assuming this is the assigned field name in your HTML form
#
#             # Check if the user with the specified Employee_Number exists
#             if User.objects.filter(Employee_Number=assigned_to).exists():
#                 print("here")
#                 newTask = Task.objects.create(
#                     Title=title,
#                     Desc=desc,
#                     Alias_Assigned=User.objects.get(Employee_Number=assigned_to),
#                     Progress=progress
#                 )
#                 newTask.save()
#                 return redirect('polls:display')
#             else:
#                 return JsonResponse({'error': 'User does not exist'}, status=400)
#         except Exception as e:
#             print(e)
#             return JsonResponse({'error': 'Error creating task'}, status=400)
#
#     return JsonResponse({'error': 'Unsupported method'}, status=405)

def task_detail(request, task_id):
    task = Task.objects.get(Task_ID=task_id)
    all_comments = Comment.objects.filter(Task_ID=task)
    return render(request, 'polls/tasks.html', {'task': task, 'comments': all_comments})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('Comment',)


@login_required
@csrf_exempt
def update_progress(request):
    print('-------')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data, "wadwad")
            taskID = data.get('taskId')
            print(taskID, '------s-----')
            newProgress = data.get('newProgress')
            task = Task.objects.get(Task_ID=taskID)
            print(task.Progress, '-------d------')
            task.Progress = newProgress
            task.save()
            print(task.Progress, '-------d2------')
            print('Done')
            return JsonResponse({'reload_page': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Unsupported method'}, status=405)


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Check if the button was clicked and update the task status
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        task.Progress = new_status
        task.save()
        return redirect('polls:display')  # Redirect to a task list view

    return render(request, 'update_task.html', {'task': task})

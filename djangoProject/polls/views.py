import json
import re

from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.models import Task, CustomerUser, Comment


# Defines a form for adding comments to a task
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('Comment',)


# Defines a form for creating a new task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Desc', 'Alias_Assigned', 'Title', 'Progress']


# Defines a form for logging a user in
class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'password']

    def clean(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid username or password.")

        return self.cleaned_data


# Defines a form for registering a user
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        missing_fields = []

        # Checks to ensure the fields are not empty
        for field_name, field_value in cleaned_data.items():
            if not field_value:
                missing_fields.append(field_name)

        # If a field is empty generates an error
        for field_name in missing_fields:
            self.add_error(field_name, "This field is required.")
        return cleaned_data

    # Ensures the password is 8 digits long, contains 1 digit, contains a special character and an uppercase letter.
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errorMessage = "Password must"
        if len(password) < 8:
            errorMessage += " be at least 8 characters long"
        if not any(char.isdigit() for char in password):
            errorMessage += "contain at least one digit"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errorMessage += " contain at least one special character '!@#$%^&*(),.?:{}|<>'"
        if not any(char.isupper() for char in password):
            errorMessage += " contain at least one uppercase letter"
        if errorMessage != "Password must":
            raise forms.ValidationError(errorMessage)
        return make_password(password)


# Authenticates that the user exists and the username and password is correct, if not returns an error
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST.get('csrfmiddlewaretoken'))
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:display')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    return render(request, 'polls/Login.html')




# Ensures all fields are filled and creates a comment for the specific task that the user is in, if not returns a suitable error.
@login_required
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


# Creates a task using the task form defined above.
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:display')
        else:
            error_messages = form.errors.as_json()
            return JsonResponse({'error': error_messages}, status=400)

    return JsonResponse({'error': 'Unsupported method'}, status=405)


# Checks if the user exists if not creates the user and provides a success message
def user_create(request):
    print("hello")
    if request.method == "POST":
        form = UserForm(request.POST)
        print("2")
        if form.is_valid():
            print("3")
            user = form.save(commit=False)
            user.password = form.cleaned_data['password']
            user.save()
            messages.success(request, 'Registration Successful')
        else:
            print("4")
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f'Error in {field}: {error}')
    return render(request, 'polls/Login.html')


# Logouts the user and redirects them to the homepage
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# Gets all the tasks made and renders them.
@login_required()
def DisplayUsers(request):
    tasks = Task.objects.all()
    return render(request, 'polls/display.html', {'Tasks': tasks})


# Gets the task information that relates to the taskID and removes it from the database.
@login_required
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


# Passes all the users into the html template
@login_required
def create_new_task_form(request):
    users = CustomerUser.objects.all()
    return render(request, 'polls/new_task.html', {'users': users})


# Gets the task information and all relating comments to a specific Task_ID and passes it to the html template
@login_required
def task_detail(request, task_id):
    task = Task.objects.get(Task_ID=task_id)
    all_comments = Comment.objects.filter(Task_ID=task)
    return render(request, 'polls/tasks.html', {'task': task, 'comments': all_comments})


@login_required
@csrf_exempt
def update_progress(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            taskID = data.get('taskId')
            newProgress = data.get('newProgress')
            task = Task.objects.get(Task_ID=taskID)
            task.Progress = newProgress
            task.save()
            return JsonResponse({'reload_page': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Unsupported method'}, status=405)


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        task.Progress = new_status
        task.save()
        return redirect('polls:display')
    return render(request, 'update_task.html', {'task': task})

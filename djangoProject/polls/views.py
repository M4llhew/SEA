# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by("-pub_date")[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"
import json

from django import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.models import Task, CustomerUser, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Desc', 'Alias_Assigned', 'Title', 'Progress']


from django import forms


class LoginForm(forms.Form):
    class Meta:
        model = CustomerUser
        fields = ['username', 'password']


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home page
                return redirect('polls:display')
            else:
                # Handle invalid login credentials
                error_message = "Invalid username or password."
        else:
            # Handle form errors
            error_message = "Invalid form data."
    else:
        form = AuthenticationForm()
        error_message = None

    return render(request, 'polls/Login.html', {'form': form, 'error_message': error_message})


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['first_name', 'last_name', 'username', 'password']


def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:Login')
        else:
            error_messages = form.errors.as_json()
            return JsonResponse({'error': error_messages}, status=400)
    return JsonResponse({'error': 'Unsupported method'}, status=405)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required()
def DisplayUsers(request):
    # if not request.user.is_authenticated:
    #     redirect('/')
    # Fetch all polls from the database
    tasks = Task.objects.all()

    # Create dictionaries to organize polls by progress
    tasks_by_progress = {
        'TODO': [],
        'INPROGRESS': [],
        'REVIEW': [],
        'DONE': [],
    }

    # Group polls by progress
    for task in tasks:
        print(task.Task_ID)
        tasks_by_progress[task.Progress].append(task)

    for progress in tasks_by_progress:
        print(progress)
        print(tasks_by_progress[progress])
        # print(task_list)
    for task in tasks:
        print("www")
        print(task.Title)
        print(task.Progress)

    # print(tasks_by_progress)
    # return render(request, 'polls/display.html', {'polls': tasks_by_progress})
    return render(request, 'polls/display.html', {'Tasks': tasks})


@login_required
@csrf_exempt
def delete_task(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            taskID = data.get('taskID')
            taskToDelete = Task.objects.get(Task_ID=taskID)
            taskToDelete.delete()
            return JsonResponse({'message': 'Progress updated successfully'})
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
# def profile(request, pk):
#     profile = Profile.objects.get(pk=pk)
#     if request.method == "POST":
#         current_user_profile = request.user.profile
#         data = request.POST
#         action = data.get("follow")
#         if action == "follow":
#             current_user_profile.follows.add(profile)
#         elif action == "unfollow":
#             current_user_profile.follows.remove(profile)
#         current_user_profile.save()
#     return render(request, "dwitter/profile.html", {"profile": profile})

# def DisplayAllCodeReviews(request):
#     formatted_crs = []
#     crs = CodeReview.objects.all()
#     for cr in crs:
#         listItem = [cr.cr_number, cr.alias, cr.package_name, cr.approved]  # Also needs the number of revisions
#         formatted_crs.append(listItem)
#     return render(request, 'polls/displayCRs.html')

#
# @csrf_exempt
# def update_employee_number(request):
#     print("TEST")
#     if request.method == 'POST':
#         print("TEST3")
#         alias = request.POST.get('alias')
#         print(alias, "WDWAD")
#         try:
#             user = User.objects.get(alias=alias)
#             user.employee_number += 1
#             user.save()
#
#             print("DONE")
#             time.sleep(4)
#             print("DONE")
#             return JsonResponse({'reload_page': True})
#         except:
#             return JsonResponse({'error': 'Not a User'}, status=400)
#     else:
#         return JsonResponse({'error': 'Not a Post'}, status=400)

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

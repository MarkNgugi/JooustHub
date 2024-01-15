from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User,Project,Projectinfo
from .forms import RoomForm, UserForm, MyUserCreationForm,ProjectForm,ProjectDetailsForm



# hubs = [

#     {'name':'ENACTUS JOOUST'},
#     {'name':'MINI MILITIA'},
#     {'name':'TECH HUB'},
# ]

# hubsortopics = [

#     {"name":'Hubs'},
#     {"name":'Topics'}
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)

def Hubs(request):
    
    context = {}
    return render(request,'base/hubs.html',context)

def hubsandtopics(request):

    context={}
    return render(request,'base/hubs&topics.html',context)

def hubshome(request):
    
    topics = Topic.objects.all()[0:5]    
    all_projects = Project.objects.all()
    public_projects = Project.objects.filter(visibility='public')
    private_projects = Project.objects.filter(visibility='private')

    all_projects_count = all_projects.count()
    public_projects_count = public_projects.count()
    private_projects_count = private_projects.count()

    visibility_filter = request.GET.get('visibility', 'all')

    if visibility_filter == 'all':
        projects = all_projects
    elif visibility_filter == 'public':
        projects = public_projects
    elif visibility_filter == 'private':
        projects = private_projects
    else:
        projects = all_projects  # Handle invalid filter values (optional)

    context = {
        'topics':topics,
        'projects': projects,
        'visibility_filter': visibility_filter,
        'all_projects_count': all_projects_count,
        'public_projects_count': public_projects_count,
        'private_projects_count': private_projects_count,
    }
    
    return render(request,'base/hubshome.html',context)


def hubprofile(request, pk):
    user = User.objects.get(id=pk)
    public_projects = Project.objects.filter(user=user, visibility='public')

    context = {
        'public_projects': public_projects,
        'user': user
    }
    return render(request, 'base/hubsprofile.html', context)


@login_required(login_url='login')
def CreateProject(request):
    user_projects_count = Project.objects.filter(user=request.user).count()

    # Check if the user has already created two projects
    if user_projects_count >= 2:
        return render(request, 'base/project_limit_exceeded.html')

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.created_by = request.user

            project.save()
            return redirect('hubshome')

    else:
        form = ProjectForm()

    context = {'form': form}
    return render(request, 'base/createproject.html', context)




@login_required(login_url='login')
def updateProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(instance=project)

    if request.user != project.user:
        return HttpResponse('You are not allowed to edit this project!!')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('hubprojectpage',pk=project.pk)

    context = {'form': form, 'project': project}
    return render(request, 'base/createproject.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if request.user != project.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        project.delete()
        return redirect('hubshome')
    return render(request, 'base/delete.html', {'obj': project})

def hubactivity(request):
    projects = Project.objects.all()
    context={'projects':projects}
    return render(request,'base/projects_activity.html',context)

def hubprojectpage(request, pk):
    # Get the selected project
    selected_project = get_object_or_404(Project, pk=pk)

    # Get all projects for the sidebar
    all_projects = Project.objects.all()

    # Filter project information based on the selected project
    projectinformation = Projectinfo.objects.filter(title=selected_project)

    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST)
        if form.is_valid():
            project_info = form.save(commit=False)
            project_info.user = request.user
            project_info.title = selected_project  # Set the selected project

            project_info.save()
            return redirect('hubprojectpage', pk=pk)
    else:
        form = ProjectDetailsForm()

    context = {
        'selected_project': selected_project,
        'all_projects': all_projects,
        'form': form,
        'projectinformation': projectinformation,
    }
    return render(request, 'base/hubprojectpage.html', context)


def mainprojectpage(request, pk):
    # Fetch the latest project details for the current user
    latest_project_details = Projectinfo.objects.filter(user=request.user, pk=pk).first()

    # Initialize the form with the latest_project_details if available
    form = ProjectDetailsForm(instance=latest_project_details) if latest_project_details else ProjectDetailsForm()

    context = {
        'form': form,
        'project_details': latest_project_details,
    }

    return render(request, 'base/mainprojectpage.html', context)


def edit_content(request, pk):
    project_info = get_object_or_404(Projectinfo, pk=pk)

    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST, instance=project_info)
        if form.is_valid():
            form.save()
            return redirect('hubprojectpage', pk=project_info.pk)
    else:
        form = ProjectDetailsForm(instance=project_info)

    context = {'form': form}
    return render(request, 'base/edit_content.html', context)


def delete_content(request, pk):
    project_info = get_object_or_404(Projectinfo, pk=pk)

    if request.method == 'POST':
        project_info.delete()
        return redirect('hubprojectpage', pk=pk)

    context = {'project_info': project_info}
    return render(request, 'base/delete_content.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        # Get the related topic and delete it
        topic = room.topic
        if topic:
            topic.delete()

        # Delete the room
        room.delete()

        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


        
        
    
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def like_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        # Check if the user already liked the project
        if request.user in project.likes.all():
            # If already liked, unlike
            project.likes.remove(request.user)
        else:
            # If not liked, like
            project.likes.add(request.user)

    return redirect('hubshome')



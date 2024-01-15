from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('home/', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),

    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),


    path('hubs/',views.Hubs,name='hubs'),
    path('hubshome/',views.hubshome,name='hubshome'),
    path('hubsandtopics/',views.hubsandtopics,name='hubsandtopics'),
    path('hubsactivity/',views.hubactivity,name='hubactivity'),

    path('create-project/',views.CreateProject,name='create-project'),
    path('hubprofile/<str:pk>/',views.hubprofile,name='hubprofile'),
    path('project/<str:pk>/', views.hubprojectpage, name='hubprojectpage'),
    path('projectpage/<str:pk>/',views.mainprojectpage,name='mainprojectpage'),

    path('project/<int:pk>/edit/', views.edit_content, name='edit_content'),
    path('project/<int:pk>/delete/', views.delete_content, name='delete_content'),
    path('like_project/<int:pk>/', views.like_project, name='like_project'),
    path('update_project/<int:pk>/', views.updateProject, name='update_project'),
    path('delete-project/<str:pk>/', views.deleteProject, name="deleteProject"),


    
]

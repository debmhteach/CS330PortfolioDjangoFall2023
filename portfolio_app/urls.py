from django.urls import path, include
from . import views


urlpatterns = [
    #path function defines a url pattern
    #'' is empty to represent based path to app
    # views.index is the function defined in views.py
    # name='index' parameter is to dynamically create url
    # example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),

    #Set up url to generic list view and detail view for students
    path('students/', views.StudentListView.as_view(), name= 'students'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),

    path('portfolios/', views.PortfolioListView.as_view(), name= 'portfolios'),
    path('portfolio/<int:pk>', views.PortfolioDetailView.as_view(), name='portfolio-detail'),

    path('projects/', views.ProjectListView.as_view(), name= 'projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),

    #Set up url for forms
    #path('create_project/', views.createProject, name='create_project'),
    path('portfolio/<int:portfolio_id>/create_project/', views.createProject, name='create_project'),
    path('portfolio/<int:portfolio_id>/update_project/<int:project_id>', views.updateProject, name='update_project'),
    path('portfolio/<int:portfolio_id>/delete_project/<int:project_id>', views.deleteProject, name='delete_project'),
    path('user/', views.userPage, name ='user_page'),
    path('portfolio/update_portfolio/<int:portfolio_id>', views.updatePortfolio, name='update_portfolio'),
    #user accounts 
    #the following include automatically maps the following urls
    #accounts/ login/ [name='login']
    #accounts/ logout/ [name='logout']
    #accounts/ password_change/ [name='password_change']
    #accounts/ password_change/done/ [name='password_change_done']
    #accounts/ password_reset/ [name='password_reset']
    #accounts/ password_reset/done/ [name='password_reset_done']
    #accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #accounts/ reset/done/ [name='password_reset_complete']
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name = 'register_page') ,
    
  
]


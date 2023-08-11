from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ProjectForm, CreateUserForm, StudentForm, PortfolioForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import  allowed_users
from django.contrib.auth.models import Group

# Create your views here.

# Render the HTML template index.html 
def index(request): 
    #get all the students
    #active_portfolios = Portfolio.objects.filter(is_active=True)
    #student_active_portfolios = Student.objects.filter(portfolio__is_active=True)
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
    #pass dictionary of students to index template tage 
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})

#implement class that inherits from a generic list view
#this will query the database to get all records

class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    
class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student



class PortfolioListView(LoginRequiredMixin, generic.ListView):
    model = Portfolio
    
class PortfolioDetailView(generic.DetailView):
    model = Portfolio

    #add more values to context to get associated projects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/
        #portfolio = Portfolio.objects.get(pk=portfolio_id)
        portfolio= self.get_object()
        print('portfolio id', portfolio)
        projects = portfolio.projectinportfolio_set.all()  # Retrieve related projects

        context["projects"] = projects
        return context


class ProjectListView(LoginRequiredMixin,generic.ListView):
    model = Project
    
class ProjectDetailView(generic.DetailView):
    model = Project

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def createProject(request, portfolio_id):
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    if request.method == 'POST':
        # Retrieve the portfolio based on the portfolio_id
        print('printing POST:', request.POST)
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()

        # Create the relationship between the project and the portfolio
            ProjectInPortfolio.objects.create(portfolio=portfolio, project = form.instance)

        # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form' :form}
    return render(request, 'portfolio_app/project_form.html', context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def updateProject(request, portfolio_id, project_id):
    project = Project.objects.get(id=project_id)
    form = ProjectForm(instance=project)
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    if request.method == 'POST':
        # Retrieve the portfolio based on the portfolio_id
        print('printing POST:', request.POST)
        print('project id:', project_id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

        # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form' :form}
    return render(request, 'portfolio_app/project_form.html', context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def updatePortfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    form = PortfolioForm(instance=portfolio)


    if request.method == 'POST':
        # Retrieve the portfolio based on the portfolio_id
        print('printing POST:', request.POST)
        print('portfolio:', portfolio_id)
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()

        # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form' :form}
    return render(request, 'portfolio_app/portfolio_form.html', context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def deleteProject(request, portfolio_id, project_id):
    project = Project.objects.get(id=project_id)
    print('portfolio_id ', portfolio_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "The project has been deleted.")
        
        return redirect('portfolio-detail', portfolio_id)
    
    context = {'item':project, 'portfolio_id':portfolio_id}
    return render(request, 'portfolio_app/project_delete.html', context)


def registerPage(request):

    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username  = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            student = Student.objects.create(user=user,) 
            portfolio = Portfolio.objects.create()  
            student.portfolio = portfolio 
            student.save()

            messages.success(request, 'Account wsa created for ' + username)
            return redirect('login')

    context ={'form':form}
    return render(request, 'registration/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userPage(request):
    student = request.user.student
    
    form = StudentForm(instance = student)
    print('student', student)
    portfolio = student.portfolio
    print(portfolio)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()

    context = {'portfolios':portfolio, 'form':form}
    #context ={}
    return render(request, 'portfolio_app/user.html', context)


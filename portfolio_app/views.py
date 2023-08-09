from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ProjectForm
from django.contrib import messages

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
class StudentListView(generic.ListView):
    model = Student
    
class StudentDetailView(generic.DetailView):
    model = Student



class PortfolioListView(generic.ListView):
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


class ProjectListView(generic.ListView):
    model = Project
    
class ProjectDetailView(generic.DetailView):
    model = Project


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


def deleteProject(request, portfolio_id, project_id):
    project = Project.objects.get(id=project_id)
    print('portfolio_id ', portfolio_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "The project has been deleted.")
        
        return redirect('portfolio-detail', portfolio_id)
    
    context = {'item':project, 'portfolio_id':portfolio_id}
    return render(request, 'portfolio_app/project_delete.html', context)
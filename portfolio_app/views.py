from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic

# Create your views here.

# Render the HTML template index.html 
def index(request): 
    #get all the students
    #active_portfolios = Portfolio.objects.filter(is_active=True)
    student_active_portfolios = Student.objects.filter(portfolio__is_active=True)
    #pass dictionary of students to index template tage 
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})

#implement class that inherits from a generic list view
#this will query the database to get all records
class StudentListView(generic.ListView):
    model = Student
    
class StudentDetailView(generic.DetailView):
    model = Student


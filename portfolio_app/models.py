from django.db import models
from django.urls import reverse

# Create your models here.

# Create project model
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default = False)
    about = models.TextField(blank = True)
    contact_email = models.CharField(max_length=200, blank = True)
    
    #project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, blank = True)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title
    
    #Returns the URL to access a particular instance of MyModelName.
    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])
    

class Student(models.Model):
    # List of choices for major value in database, human readable name
    MAJOR = (
        ("CSCI-BS", "BS in Computer Science"),
        ("CPEN-BS", "BS in Computer Engineering"),
        ("BIGD-BI", "BI in Game Design and Development"),
        ("BICS-BI", "BI in Computer Science"),
        ("BISC-BI", "BI in Computer Security"),
        ("CSCI-BA", "BA in Computer Science"),
        ("DASE-BS", "BS in Data Analytics and Systems Engineering"),
    )


    name = models.CharField(max_length=200)
    email = models.CharField("UCCS Email", max_length=200)
    major = models.CharField(max_length=200, choices=MAJOR, blank = True)

    #one student has a portfolio and each portfolio belongs to a student
    portfolio = models.OneToOneField(Portfolio, null = True, on_delete=models.CASCADE, unique=True)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.name
    
    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically 
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['name']

# In this setup, you have a separate model called ProjectInPortfolio 
# to represent the relationship between projects and portfolios. 
# Each instance of this model will have a reference to a Portfolio and a Project, 
# creating a many-to-many relationship between portfolios and projects. T
# he unique_together constraint ensures that each project is associated with a 
# portfolio only once. 
class ProjectInPortfolio(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('portfolio', 'project')
   

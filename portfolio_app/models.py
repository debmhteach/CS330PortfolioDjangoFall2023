from django.db import models

# Create your models here.

# Create project model
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default = False)
    about = models.TextField(blank = True)
    contact_email = models.CharField(max_length=200, blank = True)
    
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, blank = True)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title
    

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
    portfolio = models.OneToOneField(Portfolio, null = True, on_delete=models.CASCADE)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.name

    

   

from django.db import models

class Students(models.Model):
    student_id=models.IntegerField(unique=True)
    student_name=models.CharField(max_length=50)
    student_email=models.EmailField(unique=True)
    student_ph=models.IntegerField(unique=True)

    def __str__(self):
        return self.student_name

# Create your models here.

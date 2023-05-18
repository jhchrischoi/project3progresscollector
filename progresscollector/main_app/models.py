from django.db import models
from django.urls import reverse
# from datetime import date
from django.contrib.auth.models import User

class Recommendation(models.Model):
  drill = models.CharField(max_length=50)
  
  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('recommendations_detail', kwargs={'pk': self.id})
  
# Create your models here.
class Progress (models.Model):
    training_date = models.CharField(max_length=100)
    advice = models.CharField(max_length=100)
    goal = models.CharField(max_length=100)
    exercise = models.CharField(max_length=100)
    #M:M relationship
    recommendations = models.ManyToManyField(Recommendation)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.training_date} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'progress_id': self.id})
    
    # class Meta:
    #     ordering = ['date']

class Checklist(models.Model):
    school = models.CharField(max_length=100)
    chore = models.CharField(max_length=100)
    rest = models.CharField(max_length=100)
    # school work
    # 1 house chore
    # ate & slept well
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for progress_id: {self.progress_id} @{self.url}"
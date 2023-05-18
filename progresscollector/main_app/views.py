import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from. models import Progress, Recommendation, Photo
from .forms import ChecklistForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgressList(ListView):
   model = Progress
   
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def progresses_index(request):
    progresses = Progress.objects.filter(user=request.user)
    return render(request, 'progresses/index.html', 
    { 
        'progresses': progresses 
    }
)

@login_required
def progresses_detail(request, progress_id):
  progress = Progress.objects.get(id=progress_id)
  id_list = progress.recommendations.all().values_list('id')
  recommendations_progress_doesnt_have = Recommendation.objects.exclude(id__in=id_list)
  checklist_form = ChecklistForm()
  return render(request, 'progresses/detail.html', { 'progress': progress,
    'checklist_form': checklist_form, 'recommendations':recommendations_progress_doesnt_have
    })

class ProgressCreate(LoginRequiredMixin, CreateView):
  model = Progress
  fields = ['training_date','advice','goal','exercise']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ProgressUpdate(LoginRequiredMixin, UpdateView):
  model = Progress
  fields = ['advice', 'goal', 'exercise']

class ProgressDelete(LoginRequiredMixin, DeleteView):
  model = Progress
  success_url = '/progress'

@login_required
def add_checklist(request, progress_id):
  form = ChecklistForm(request.POST)
  if form.is_valid():
    new_checklist = form.save(commit=False)
    new_checklist.progress_id=progress_id
    new_checklist.save()
  return redirect('detail', progress_id=progress_id)

class RecommendationList(LoginRequiredMixin, ListView):
  model = Recommendation

class RecommendationDetail(LoginRequiredMixin, DetailView):
  model = Recommendation

class RecommendationCreate(LoginRequiredMixin, CreateView):
  model = Recommendation
  fields = '__all__'

class RecommendationUpdate(LoginRequiredMixin, UpdateView):
  model = Recommendation
  fields = ['drill']

class RecommendationDelete(LoginRequiredMixin, DeleteView):
  model = Recommendation
  success_url = '/recommendations'

@login_required
def assoc_recommendation(request, progress_id, recommendation_id):
  Progress.objects.get(id=progress_id).recommendations.add(recommendation_id)
  return redirect('detail', progress_id=progress_id)

@login_required
def unassoc_recommendation(request, progress_id, recommendation_id):
  Progress.objects.get(id=progress_id).recommendations.remove(recommendation_id)
  return redirect('detail', progress_id=progress_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, progress_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, progress_id=progress_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', progress_id=progress_id)
from django.forms import ModelForm
from .models import Checklist

class ChecklistForm(ModelForm):
  class Meta:
    model = Checklist
    fields = ['school', 'chore', 'rest']
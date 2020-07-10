from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import Client, Trainer, User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ('sport', 'location')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('goal', 'gender', 'height', 'weight')
from django.shortcuts import get_object_or_404, render
from .models import Client, Trainer


def profile_client(request, username):
    client = get_object_or_404(Client, username=username)
    return render(request, "client_profile.html", {"client": client})


def profile_trainer(request, username):
    trainer = get_object_or_404(Trainer, username=username)
    return render(request, "trainer_profile.html", {"trainer": trainer})
from django.shortcuts import render, redirect

from .forms import CreationForm, TrainerForm, ClientForm


def signup(request, signup_type):
    signup_types = {
        'trainer': TrainerForm,
        'client': ClientForm
    }

    if signup_type in signup_types:
        form_generic = signup_types[signup_type]
    else:
        return redirect('signup_choice')

    if request.method == 'POST':
        user_form = CreationForm(request.POST)
        user_type_form = form_generic(request.POST)
        if user_form.is_valid() and user_type_form.is_valid():
            user = user_form.save()
            user_type_form.save()
            return redirect('profile', kwargs={signup_type: user.username})

    else:
        user_form = CreationForm()
        user_type_form = form_generic()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'user_type_form': user_type_form
    })


def signup_choice(request):
    return render(request, 'signup_choice.html')
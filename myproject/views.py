from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    users = User.objects.all()

    context = {
        'users': users,

    }
    return render(request,"index.html", context)
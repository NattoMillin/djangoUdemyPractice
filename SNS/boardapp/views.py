from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from .models import BoardModel
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


# Create your views here.


def signupfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(username, "", password)
            return render(request, "login.html", {"some": "100"})
        except IntegrityError:
            print("Error")
            return render(
                request, "signup.html", {"error": "このユーザー名は登録済みです。"}
            )
    return render(request, "signup.html")


def loginfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("list")
        else:
            return render(request, "login.html", {})
    return render(request, "login.html", {})


@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()

    return render(request, "list.html", {"object_list": object_list})


def logoutfunc(request):
    logout(request)
    return redirect("login")


def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    return render(request, "detail.html", {"object": object})


def goodfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    object.good += 1
    object.save()
    return redirect("list")


def readfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect("list")
    else:
        object.read += 1
        object.readtext += " " + username
        object.save()
        return redirect("list")


class BoardCreate(CreateView):
    model = BoardModel
    template_name = "create.html"
    fields = ("title", "content", "author", "snsimage")
    success_url = reverse_lazy("list")

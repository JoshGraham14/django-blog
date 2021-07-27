from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm, CreateUserForm
from .decorators import unauthenticated_user, login_needed


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect('login_page')

    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_needed
def index(request):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context = {'post_list': queryset}
    return render(request, 'index.html', context)


@login_needed
def new_post(request):
    form = PostForm(user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}

    return render(request, 'newpost.html', context)


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'editpost.html'
    fields = ['title', 'content']


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug)
    context = {'post': post[0], 'user': request.user}
    return render(request, 'postdetail.html', context)


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'postdetail.html'

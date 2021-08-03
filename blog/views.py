from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm, CreateUserForm
from .decorators import unauthenticated_user, login_needed
from django.http import Http404


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
    """View to edit/update Posts"""
    model = Post
    template_name = 'editpost.html'
    form_class = PostForm

    def get_form_kwargs(self):
        """Retrieves the request.user kwarg for the PostForm __init__ method"""
        kwargs = super(UpdatePostView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        """Ensures that only the author is allowed to edit the post"""
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404(
                'You are not allowed to edit this post because you are not the author.')
        return super(UpdatePostView, self).dispatch(request, *args, **kwargs)


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug)
    context = {'post': post[0], 'user': request.user}
    return render(request, 'postdetail.html', context)


def post_delete(request, slug):
    post = Post.objects.filter(slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('/')
    context = {'post': post}
    return render(request, 'index.html', context)

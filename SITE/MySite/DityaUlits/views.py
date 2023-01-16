from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *

class DityaUlitsHome(DataMixin, ListView):
    model = Project
    template_name = "DityaUlits/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Project.objects.filter(is_published=True)

#def index(request):
#    posts = Project.objects.all()
#
#    context = {
#        'posts': posts,
#        'menu': menu,
#        'title': 'Главная страница',
#        'cat_selected' : 0,
#    }
#    return render(request,'DityaUlits/index.html', context=context)

def about(request):
    return render(request,'DityaUlits/about.html', {'title':'О сайте'})

# def addpage(request):
#     #def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'DityaUlits/addpage.html', {'form':form, 'menu': menu, 'title': 'Добавление статьи'})

class AddPage(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'DityaUlits/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))

def contact(request):
    return HttpResponse("Обратная связь")

# def login(request):
#     return HttpResponse("Авторизация")

# def show_post(request, post_slug):
#     post = get_object_or_404(Project, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'DityaUlits/post.html', context=context)

class ShowPost(DataMixin,DetailView):
    model = Project
    template_name = 'DityaUlits/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')

# def show_category(request, cat_id):
#     posts = Project.objects.filter(cat_id=cat_id)
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'DityaUlits/index.html', context=context)

class ProjectCategory(DataMixin, ListView):
    model = Project
    template_name = 'DityaUlits/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Project.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'DityaUlits/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# class LoginUserForm:
#     pass


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'DityaUlits/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Tasks

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name= 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get( *args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista'] = context['lista'].filter(usuario=self.request.user)
        context['count'] = context['lista'].filter(completado= False).count()
        
        
        s_busqueda = self.request.GET.get('Buscar-area') or ''
        if s_busqueda:
            context['lista'] =context['lista'].filter(titulo__icontains =s_busqueda )
        context['s_busqueda'] = s_busqueda
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    context_object_name = 'detalle'
    template_name ='base/detalle.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    fields = ['titulo', 'descripcion', 'completado']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['titulo', 'descripcion', 'completado']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'detalle'
    success_url = reverse_lazy('tasks')



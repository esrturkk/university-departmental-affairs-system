from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

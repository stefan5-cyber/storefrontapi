from django.core.mail import EmailMessage, BadHeaderError
from django.views.generic import TemplateView
from django.http import HttpResponse


class HomeView(TemplateView):
    template_name = 'page/home.html'

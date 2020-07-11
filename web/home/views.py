from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0} has sent you a new message:\n\n{2}\n\n{1}".format(
                sender_name, form.cleaned_data['message'], sender_email)
            send_mail('New Enquiry', message, sender_email,
                      ['teamfinatic3@gmail.com'])
            return HttpResponse('Thanks for contacting us!')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def home(request):
    return render(request, "home.html")


def team(request):
    return render(request, "team.html")


def about(request):
    return render(request, "about.html")


def base(request):
    return render(request, 'base.html')


def result(request, ):
    return render(request, "result.html")

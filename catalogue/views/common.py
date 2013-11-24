from django.shortcuts import render_to_response

from catalogue.models import BookCathegory


def index(request):
    book_cathegory_list = BookCathegory.objects.filter(active=True).order_by('-cathegory_name')
    return render_to_response('catalogue/templates/index.html', {'book_cathegory_list': book_cathegory_list})

def sitemanagement(request):#its temporary, shold be replated with google oauth2
    book_cathegory_list = BookCathegory.objects.filter(active=True).order_by('-cathegory_name')
    return render_to_response('catalogue/templates/site_management.html', {'book_cathegory_list': book_cathegory_list})

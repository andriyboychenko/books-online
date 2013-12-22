from django.shortcuts import render_to_response

from catalogue.models import BookCategory
from catalogue.entities import RU_ru


def index(request):
    book_category_list = BookCategory.objects.filter(active=True).order_by('category_name')
    return render_to_response('catalogue/templates/index.html', {'book_category_list': book_category_list})

def sitemanagement(request):#its temporary, shold be replated with google oauth2
    book_category_list = BookCategory.objects.filter(active=True).order_by('category_name')
    return render_to_response('catalogue/templates/site-management.html', {'book_category_list': book_category_list, 'lang': RU_ru})

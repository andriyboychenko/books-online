from django.shortcuts import render_to_response

from catalogue.models import BookCategory, BookAttribute, BookAttributeType
from catalogue.entities import RU_ru


def index(request):
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('category_name')
    return render_to_response('catalogue/templates/index.html', 
                              {'book_category_list': bookCategoryList})

def sitemanagement(request):#its temporary, shold be replated with google oauth2
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    return render_to_response('catalogue/templates/site-management.html', 
                              {'book_category_list': bookCategoryList, 
                               'lang': RU_ru})

def covermanagement(request):
    attributeType = BookAttributeType.objects.filter(type_name = "cover", active = True)[0] #TODO: type name should be in constants
    bookCoverList = BookAttribute.objects.filter(attribute_type = attributeType, active = True).order_by('-db_insert_date')
    return render_to_response('catalogue/templates/book-cover-management.html', 
                              {'book_cover_list': bookCoverList,
                               'lang': RU_ru})

def qualitymanagement(request):
    attributeType = BookAttributeType.objects.filter(type_name = "quality", active = True)[0] #TODO: type name should be in constants
    bookQualityList = BookAttribute.objects.filter(attribute_type = attributeType, active = True).order_by('-db_insert_date')
    return render_to_response('catalogue/templates/book-quality-management.html', 
                              {'book_quality_list': bookQualityList, 
                               'lang': RU_ru})

def languagemanagement(request):
    attributeType = BookAttributeType.objects.filter(type_name = "language", active = True)[0] #TODO: type name should be in constants
    bookLanguageList = BookAttribute.objects.filter(attribute_type = attributeType, active = True).order_by('-db_insert_date')
    return render_to_response('catalogue/templates/book-language-management.html', 
                              {'book_language_list': bookLanguageList, 
                               'lang': RU_ru})

def bookmanagement(request):
    #TODO: get book list
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    
    #TODO: type name should be in constants
    attributeTypeCover = BookAttributeType.objects.filter(type_name = "cover", active = True)[0] 
    attributeTypeQuality = BookAttributeType.objects.filter(type_name = "quality", active = True)[0] 
    attributeTypeLanguage = BookAttributeType.objects.filter(type_name = "language", active = True)[0] 
    bookCoverList = BookAttribute.objects.filter(attribute_type = attributeTypeCover, active = True).order_by('-db_insert_date')
    bookQualityList = BookAttribute.objects.filter(attribute_type = attributeTypeQuality, active = True).order_by('-db_insert_date')
    bookLanguageList = BookAttribute.objects.filter(attribute_type = attributeTypeLanguage, active = True).order_by('-db_insert_date')

    return render_to_response('catalogue/templates/book-management.html', 
                                {'book_list': None, 
                                'book_category_list': bookCategoryList,
                                'book_cover_list': bookCoverList,
                                'book_quality_list': bookQualityList, 
                                'book_language_list': bookLanguageList, 
                                'lang': RU_ru})

def bookaddnew(request):
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    
    #TODO: type name should be in constants
    attributeTypeCover = BookAttributeType.objects.filter(type_name = "cover", active = True)[0] 
    attributeTypeQuality = BookAttributeType.objects.filter(type_name = "quality", active = True)[0] 
    attributeTypeLanguage = BookAttributeType.objects.filter(type_name = "language", active = True)[0] 
    bookCoverList = BookAttribute.objects.filter(attribute_type = attributeTypeCover, active = True).order_by('-db_insert_date')
    bookQualityList = BookAttribute.objects.filter(attribute_type = attributeTypeQuality, active = True).order_by('-db_insert_date')
    bookLanguageList = BookAttribute.objects.filter(attribute_type = attributeTypeLanguage, active = True).order_by('-db_insert_date')

    return render_to_response('catalogue/templates/book-add-new.html', 
                                {'book_list': None, 
                                'book_category_list': bookCategoryList,
                                'book_cover_list': bookCoverList,
                                'book_quality_list': bookQualityList, 
                                'book_language_list': bookLanguageList, 
                                'lang': RU_ru})
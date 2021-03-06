from django.shortcuts import render_to_response

from catalogue.models import BookItem, BookCategory, BookAttribute, BookAttributeType
from catalogue.entities import RU_ru
from django.conf import settings


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
    bookItemList = BookItem.objects.filter(active=True).order_by('-db_insert_date')
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    
    #TODO: type name should be in constants
    attributeTypeCover = BookAttributeType.objects.filter(type_name = "cover", active = True)[0] 
    attributeTypeQuality = BookAttributeType.objects.filter(type_name = "quality", active = True)[0] 
    attributeTypeLanguage = BookAttributeType.objects.filter(type_name = "language", active = True)[0] 
    bookCoverList = BookAttribute.objects.filter(attribute_type = attributeTypeCover, active = True).order_by('-db_insert_date')
    bookQualityList = BookAttribute.objects.filter(attribute_type = attributeTypeQuality, active = True).order_by('-db_insert_date')
    bookLanguageList = BookAttribute.objects.filter(attribute_type = attributeTypeLanguage, active = True).order_by('-db_insert_date')

    return render_to_response('catalogue/templates/book-management.html', 
                                {'book_list': bookItemList, 
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
                                {
                                'book_category_list': bookCategoryList,
                                'book_cover_list': bookCoverList,
                                'book_quality_list': bookQualityList, 
                                'book_language_list': bookLanguageList, 
                                'lang': RU_ru})

def bookedit(request, bookid):
    
    bookCategoryList = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    
    #TODO: type name should be in constants
    bookitem = BookItem.objects.filter(book_uuid = bookid, active = True)[0]
    bookitem.book_images_names = eval(bookitem.book_images_names)
    attributeTypeCover = BookAttributeType.objects.filter(type_name = "cover", active = True)[0] 
    attributeTypeQuality = BookAttributeType.objects.filter(type_name = "quality", active = True)[0] 
    attributeTypeLanguage = BookAttributeType.objects.filter(type_name = "language", active = True)[0] 
    bookCoverList = BookAttribute.objects.filter(attribute_type = attributeTypeCover, active = True).order_by('-db_insert_date')
    bookQualityList = BookAttribute.objects.filter(attribute_type = attributeTypeQuality, active = True).order_by('-db_insert_date')
    bookLanguageList = BookAttribute.objects.filter(attribute_type = attributeTypeLanguage, active = True).order_by('-db_insert_date')
        
    return render_to_response('catalogue/templates/book-add-new.html', 
                                {'book_item': bookitem, 
                                'book_category_list': bookCategoryList,
                                'book_cover_list': bookCoverList,
                                'book_quality_list': bookQualityList, 
                                'book_language_list': bookLanguageList, 
                                'IMAGES_IN_SCROLL': settings.IMAGES_IN_SCROLL,
                                'THUMBNAIL_X': settings.IMAGE_THUMBNAIL[0],
                                'THUMBNAIL_Y': settings.IMAGE_THUMBNAIL[1],
                                'lang': RU_ru})
    
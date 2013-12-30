import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json
from django.core import serializers

from catalogue.entities import ResponseMessages
from catalogue.utils.management.BookCategoryUtils import BookCategoryUtils

from catalogue.models import BookCategory, User
from catalogue.entities import RU_ru

log = logging.getLogger("django")

def remove(request):
    object_id = request.POST["object_id"]
    action_response = {}
    
    try:
        users = User.objects.filter(id=1) #TODO: hardcoded
        
        if len(users) > 0:
            modifyUser = users[0]
                        
            categoryUtils = BookCategoryUtils()
            isRemoved = categoryUtils.removeCategory(object_id, modifyUser)
            if isRemoved:
                action_response['status'] = 1 #1-ok, 2-warn, 3-error
            else:
                action_response['status'] = 3 #1-ok, 2-warn, 3-error
        
    except Exception as error:
        log.error(error)
        action_response['status'] = 3
    
    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response


def insert_book_category(request):
    
    book_category_name_txt = request.POST["book-category-name-txt"]
    book_category_desc_txt = request.POST["book-category-desc-txt"]
    super_category_select = request.POST["super-category-select"]
    book_category_id = request.POST["book-category-id"]
        
    status_code = 1 #1-ok, 2-warn, 3-error
    
    try:
        users = User.objects.filter(id=1) #TODO: hardcoded
        
        if len(users) > 0:
            modify_user = users[0]
                        
            categoryUtils = BookCategoryUtils()
            
            # Modify book category
            if len(book_category_id) > 0:
                isModified = categoryUtils.modifyCategory(
                                 book_category_id,
                                 book_category_name_txt,
                                 book_category_desc_txt,
                                 super_category_select,
                                 modify_user)
                if not isModified:
                    status_code = 3
                    
            # Add new book category
            else:
                isInserted = categoryUtils.addNewCategory(book_category_name_txt,
                                 book_category_desc_txt,
                                 super_category_select,
                                 modify_user)
                if not isInserted:
                    status_code = 3
                
    except Exception as error:
        log.error(error)
        status_code = 3
        
    book_category_list = BookCategory.objects.filter(active=True).order_by('-db_insert_date')
    
    return render_to_response(
                              'catalogue/templates/site-management.html', 
                              {
                               'book_category_list': book_category_list, 
                               'status': status_code,
                               'lang': RU_ru
                               })



def valid_name(request):
            
    fieldValue = request.GET["field_value"]
    bookCategoryId = request.GET["edit_id"]
        
    action_response = {}
                
    try:
        categoryWithSameName = BookCategory.objects.filter(category_name = fieldValue, active=True)

        # When we adding new book category
        if bookCategoryId == '':
            if len(categoryWithSameName) == 0:
                action_response['isExists'] = "false"
            else: 
                action_response['isExists'] = "true"  
        # When we are editing book category
        else:
            currentCategory = BookCategory.objects.filter(id = bookCategoryId, active=True)
            action_response['isExists'] = "true"
            
            if len(categoryWithSameName) == 0:
                action_response['isExists'] = "false"
            elif len(currentCategory) > 0:
                if currentCategory[0].id == categoryWithSameName[0].id:
                    action_response['isExists'] = "false"
                    
    except Exception as error:
        log.error(error)
        action_response['isExists'] = "true" #TODO: send the specific error message or it is anought?

    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response



def edit_load_data(request):
    
    categoryId = request.GET["current_id"]
    action_response = {}
    
    try:
        editBookCategory = BookCategory.objects.filter(id=categoryId)
        action_response['status'] = 1
        response_data = serializers.serialize('json', editBookCategory, fields=(
                                                                                  'category_name',
                                                                                  'category_description',
                                                                                  'sub_category_of'))
        #response_data = json.dumps(editBookCategory)
        #response_data += json.dumps(action_response)
        
    
    except Exception as error:
        log.error(error)
        action_response['status'] = 3
        response_data = json.dumps(action_response)
    
    response = HttpResponse()
    response.write(response_data)
    
    return response





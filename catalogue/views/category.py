from django.shortcuts import render_to_response
from django.utils import timezone
from django.http import HttpResponse
from django.utils import simplejson as json


from catalogue.entities import ResponseMessages


from catalogue.models import BookCategory, User



def bookdetail(request, book_id):
    #https://docs.djangoproject.com/en/1.4/intro/tutorial03/#raising-404
    try:
        print "do nothing"
        #p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('catalogue/templates/detail.html', {'poll': p})

def remove(request):
    object_id = request.POST["object_id"]
    
    action_response = {}
    
    try:
        book_category = BookCategory.objects.filter(id=object_id)[0] 
        book_category.active = False
        book_category.save()
            
        action_response['status'] = 1 #1-ok, 2-warn, 3-error
    except Exception as error:
        print error
        action_response['status'] = 3
    
    
    
    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response

#
#TODO: https://docs.djangoproject.com/en/dev/topics/forms/
#reposts on refresh should be avoided
#


def insert_book_category(request):
    
    book_category_name_txt = request.POST["book-category-name-txt"]
    book_category_desc_txt = request.POST["book-category-desc-txt"]
    super_category_select = request.POST["super-category-select"]
    
    status_code = 1 #1-ok, 2-warn, 3-error
    
    try:
        
        users = User.objects.filter(id=1) #TODO: hardcoded
        if len(users) > 0:
                
            modify_user = users[0]
            
            check_if_exists = BookCategory.objects.filter(category_name=book_category_name_txt, active=True)

            if len(check_if_exists) == 0:
            
                #User haven't selected super category
                if len(super_category_select) == 0:
                    category = BookCategory(
                                              category_name=book_category_name_txt,
                                              category_description=book_category_desc_txt,
                                              db_insert_date=timezone.now(), 
                                              db_modify_date=timezone.now(), 
                                              db_modify_user=modify_user)
                    
                else:
                    super_category = BookCategory.objects.filter(id=super_category_select, active=True)[0]
                    category = BookCategory(
                                              category_name=book_category_name_txt, 
                                              category_description=book_category_desc_txt, 
                                              sub_category_of=super_category, 
                                              db_insert_date=timezone.now(), 
                                              db_modify_date=timezone.now(), 
                                              db_modify_user=modify_user)
    
                category.save()
            
            else:
                #retun error to the fronend
                print "category exits"

    except Exception as error:
        print error
        status_code = 3
        
    book_category_list = BookCategory.objects.filter(active=True).order_by('category_name')
    
    return render_to_response(
                              'catalogue/templates/site-management.html', 
                              {
                               'book_category_list': book_category_list, 
                               'status': status_code
                               })



def valid_name(request):
    
    print "exec!"
    
    field_value = request.GET["field_value"]
    
    action_response = {}

    check_if_exists = BookCategory.objects.filter(category_name=field_value, active=True)
   
    if len(check_if_exists) == 0:
        action_response['isExists'] = "false" # 1-yes or 0-no
    else: 
        action_response['isExists'] = "true"

    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response






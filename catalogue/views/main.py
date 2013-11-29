from django.shortcuts import render_to_response
from django.utils import timezone
from django.http import HttpResponse
from django.utils import simplejson as json


from catalogue.entities import ResponseMessages


from catalogue.models import BookCathegory, User



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
    object_type = request.POST["object_type"]
    
    action_response = {}
    
    try:
        if object_type == "bookCathegory":
            book_cathegory = BookCathegory.objects.filter(id=object_id)[0] 
            book_cathegory.active = False
            book_cathegory.save()
            
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


def insert_book_cathegory(request):
    
    book_cathegory_name_txt = request.POST["book-cathegory-name-txt"]
    book_cathegory_desc_txt = request.POST["book-cathegory-desc-txt"]
    super_cathegory_select = request.POST["super-cathegory-select"]
    
    status_code = 1 #1-ok, 2-warn, 3-error
    
    try:
        
        users = User.objects.filter(id=1) #TODO: hardcoded
        if len(users) > 0:
                
            modify_user = users[0]
            
            check_if_exists = BookCathegory.objects.filter(cathegory_name=book_cathegory_name_txt, active=True)

            if len(check_if_exists) == 0:
            
                #User haven't selected super cathegory
                if len(super_cathegory_select) == 0:
                    cathegory = BookCathegory(
                                              cathegory_name=book_cathegory_name_txt,
                                              cathegory_description=book_cathegory_desc_txt,
                                              db_insert_date=timezone.now(), 
                                              db_modify_date=timezone.now(), 
                                              db_modify_user=modify_user)
                    
                else:
                    super_cathegory = BookCathegory.objects.filter(id=super_cathegory_select, active=True)[0]
                    cathegory = BookCathegory(
                                              cathegory_name=book_cathegory_name_txt, 
                                              cathegory_description=book_cathegory_desc_txt, 
                                              sub_cathegory_of=super_cathegory, 
                                              db_insert_date=timezone.now(), 
                                              db_modify_date=timezone.now(), 
                                              db_modify_user=modify_user)
    
                cathegory.save()
            
            else:
                #retun error to the fronend
                print "cathegory exits"

    except Exception as error:
        print error
        status_code = 3
        
    book_cathegory_list = BookCathegory.objects.filter(active=True).order_by('cathegory_name')
    
    return render_to_response(
                              'catalogue/templates/site_management.html', 
                              {
                               'book_cathegory_list': book_cathegory_list, 
                               'status': status_code
                               })











from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json


from catalogue.entities import ResponseMessages


from catalogue.models import BookCathegory



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
            print "deleting cathegory"
            
        action_response['status'] = 1 #1-ok, 2-warn, 3-error
    except :
        action_response['status'] = 3
    
    
    
    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response

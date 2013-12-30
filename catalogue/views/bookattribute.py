import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json
from django.core import serializers

from catalogue.models import BookAttribute, BookAttributeType, User
from catalogue.entities import RU_ru

from catalogue.utils.management.BookAttributeUtils import BookAttributeUtils


log = logging.getLogger("django")


def remove(request):
    attributeId = request.POST["object_id"]
    attributeType = request.POST["attribute_type"]
    action_response = {}
    
    users = User.objects.filter(id=1) #TODO: hardcoded
        
    if len(users) > 0:
        modifyUser = users[0]
        try:
            attributeUtils = BookAttributeUtils()
            attributeUtils.removeAttribute(attributeId, attributeType, modifyUser)
            action_response['status'] = 1 #1-ok, 2-warn, 3-error
            
        except Exception as error:
            log.error(error)
            action_response['status'] = 3
    
    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response

def insertBookAttribute(request):
    bookAttributeNameTxt = request.POST["book-attribute-name-txt"]
    bookAttributeDescription = request.POST["book-attribute-desc-txt"]
    bookAttributeId = request.POST["book-attribute-id"]
    attributeType = request.POST["attribute-type"]
        
    statusCode = 1 #1-ok, 2-warn, 3-error
    
    try:
        users = User.objects.filter(id=1) #TODO: hardcoded
        
        if len(users) > 0:
            modifyUser = users[0]     
            attributesUtils = BookAttributeUtils()
            
            # Modify attribute
            if len(bookAttributeId) > 0:
                isModified = attributesUtils.modifyAttribute(
                                 bookAttributeId,
                                 bookAttributeNameTxt,
                                 bookAttributeDescription,
                                 modifyUser)
                if not isModified:
                    statusCode = 3
                    
            # Add new attribute
            else:
                isInserted = attributesUtils.addNewAttribute(bookAttributeNameTxt,
                                bookAttributeDescription,
                                attributeType,
                                modifyUser)
                if not isInserted:
                    statusCode = 3
                
    except Exception as error:
        log.error(error)
        statusCode = 3
        
    attributeType = BookAttributeType.objects.filter(type_name = attributeType, active = True)[0]
    bookAttributeList = BookAttribute.objects.filter(attribute_type = attributeType, active = True).order_by('-db_insert_date')
    
    #TODO: in case of error should redirect to error page
    responseUrls = {"cover"     :"catalogue/templates/book-cover-management.html",
                    "quality"   :"catalogue/templates/book-quality-management.html",
                    "language"  :"catalogue/templates/book-language-management.html"}
    responseResultName = {"cover"     :"book_cover_list",
                          "quality"   :"book_quality_list",
                          "language"  :"book_language_list"}

    return render_to_response(responseUrls[str(attributeType)], 
                              {
                               responseResultName[str(attributeType)]: bookAttributeList, 
                               'status': statusCode,
                               'lang': RU_ru
                               })


def validName(request):          
    fieldValue = request.GET["field_value"]
    bookAttributeId = request.GET["edit_id"]
    attributeType = request.GET["attribute_type"]
    action_response = {}
                
    try:
        bookAttributeType = BookAttributeType.objects.filter(type_name = attributeType)[0]
        attributeWithSameName = BookAttribute.objects.filter(attribute_name = fieldValue, 
                                                             attribute_type = bookAttributeType, 
                                                             active=True)

        # When we adding new book attribute
        if bookAttributeId == '':
            if len(attributeWithSameName) == 0:
                action_response['isExists'] = "false"
            else: 
                action_response['isExists'] = "true"  
        # When we are editing book attribute
        else:
            currentAttribute = BookAttribute.objects.filter(id = bookAttributeId, active=True)
            action_response['isExists'] = "true"
            
            if len(attributeWithSameName) == 0:
                action_response['isExists'] = "false"
            elif len(currentAttribute) > 0:
                if currentAttribute[0].id == attributeWithSameName[0].id:
                    action_response['isExists'] = "false"
                    
    except Exception as error:
        log.error(error)
        action_response['isExists'] = "true" #TODO: send the specific error message or it is anought?

    response_data = json.dumps(action_response)
    response = HttpResponse()
    response.write(response_data)
    
    return response



def loadEditData(request):
    attributeId = request.GET["current_id"]
    action_response = {}
    
    try:
        editBookAttribute = BookAttribute.objects.filter(id=attributeId)
        action_response['status'] = 1
        response_data = serializers.serialize('json', editBookAttribute, fields=('attribute_name',
                                                                                 'attribute_description'))
        #response_data = json.dumps(editBookCategory)
        #response_data += json.dumps(action_response)
        
    
    except Exception as error:
        log.error(error)
        action_response['status'] = 3
        response_data = json.dumps(action_response)
    
    response = HttpResponse()
    response.write(response_data)
    
    return response
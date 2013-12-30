import logging

from django.utils import timezone
from catalogue.models import BookAttribute, BookAttributeType

log = logging.getLogger("django")

class BookAttributeUtils:
    
    def removeAttribute(self, bookAttributeId, attributeTypeName, modifyUser):
        bookAttributeType = BookAttributeType.objects.filter(type_name = attributeTypeName)[0]
        bookAttribute = BookAttribute.objects.filter(id = bookAttributeId, attribute_type = bookAttributeType)
        
        if len(bookAttribute) > 0:
            bookAttribute[0].active = False
            bookAttribute[0].modifyUser = modifyUser
            bookAttribute[0].save()
        else:
            log.warning("Cannot remove attribute. Attribute no more longger exists")
            return False
        return True
        
        
    def addNewAttribute(self, bookAttributeName, bookAttributeDescription, attributeType, modifyUser):
        bookAttributeType = BookAttributeType.objects.filter(type_name = attributeType)[0]
        attributeWithSameName = BookAttribute.objects.filter(attribute_name = bookAttributeName, 
                                                             attribute_type = bookAttributeType, 
                                                             active = True)
        if len(attributeWithSameName) == 0:
            attribute = BookAttribute(
                attribute_name = bookAttributeName,
                attribute_type = bookAttributeType,
                attribute_description = bookAttributeDescription,
                db_insert_date = timezone.now(), 
                db_modify_date = timezone.now(), 
                db_modify_user = modifyUser)
            attribute.save()
        else:
            log.warning("Cannot insert new attribute. Attribute with same name already exits")
            return False
        return True    
            
        
    def modifyAttribute(self, bookAttributeId, bookAttributeName, bookAttributeDescription, modifyUser):
        print bookAttributeId
        currentAttribute = BookAttribute.objects.filter(id = bookAttributeId, active = True)
        attributeWithSameName = BookAttribute.objects.filter(attribute_name = bookAttributeName, active = True)
        
        canProceed = False
        if len(attributeWithSameName) == 0:
            canProceed = True
        elif len(currentAttribute) > 0 and len(attributeWithSameName) > 0:
            if currentAttribute[0].id == attributeWithSameName[0].id:
                canProceed = True
             
        if canProceed:
            print bookAttributeName
            print bookAttributeDescription
            print modifyUser
            currentAttribute[0].attribute_name = bookAttributeName
            currentAttribute[0].attribute_description = bookAttributeDescription
            currentAttribute[0].db_modify_date = timezone.now()
            currentAttribute[0].modifyUser = modifyUser
            currentAttribute[0].save() 
            
        else:
            log.warning("Cannot modify new category. Category with same name already exits")
            return False
        
        return True
        
        
        
        
        
        
        
        
        
        
        
        
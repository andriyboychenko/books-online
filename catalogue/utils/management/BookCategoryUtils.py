import logging

from django.utils import timezone
from catalogue.models import BookCategory

log = logging.getLogger("django")

class BookCategoryUtils:
    
    def removeCategory(self, bookCategoryId, modifyUser):
        bookCategory = BookCategory.objects.filter(id=bookCategoryId)
        
        if len(bookCategory) > 0:
            bookCategory[0].active = False
            bookCategory[0].modifyUser = modifyUser
            bookCategory[0].save()
        else:
            log.warning("Cannot remove category. Category no more longger exists")
            return False
        return True
        
        
        
    def addNewCategory(self, bookCategoryName, bookCategoryDesc, superCategoryId, modifyUser):
        categoryWithSameName = BookCategory.objects.filter(category_name=bookCategoryName, active=True)
        
        if len(categoryWithSameName) == 0:
            
            #User haven't selected super category
            if len(superCategoryId) == 0:
                category = BookCategory(
                  category_name = bookCategoryName,
                  category_description = bookCategoryDesc,
                  db_insert_date = timezone.now(), 
                  db_modify_date = timezone.now(), 
                  db_modify_user = modifyUser)
            else:
                superCategory = BookCategory.objects.filter(id = superCategoryId, active = True)
                
                if len(superCategory) > 0:
                    category = BookCategory(
                      category_name = bookCategoryName, 
                      category_description = bookCategoryDesc, 
                      sub_category_of = superCategory[0], 
                      db_insert_date = timezone.now(), 
                      db_modify_date = timezone.now(), 
                      db_modify_user = modifyUser)
                else:
                    log.warning("Cannot insert new category. Super category no more longger exists")
                    return False

            category.save()
        else:
            log.warning("Cannot insert new category. Category with same name already exits")
            return False
        return True    

            
            
    def modifyCategory(self, bookCategoryId, bookCategoryName, bookCategoryDesc, superCategoryId, modifyUser):
        currentCategory = BookCategory.objects.filter(id = bookCategoryId, active = True)
        categoryWithSameName = BookCategory.objects.filter(category_name = bookCategoryName, active = True)
        
        canProceed = False
        if len(categoryWithSameName) == 0:
            canProceed = True
        elif len(currentCategory) > 0 and len(categoryWithSameName) > 0:
            if currentCategory[0].id == categoryWithSameName[0].id:
                canProceed = True
                
        if canProceed:
            category = currentCategory[0]
            
            #User haven't selected super category
            if len(superCategoryId) == 0:
                category.category_name = bookCategoryName
                category.category_description = bookCategoryDesc
                category.db_modify_date = timezone.now()
                category.modifyUser = modifyUser
            else:
                category.category_name = bookCategoryName
                category.category_description = bookCategoryDesc
                category.sub_category_of = superCategoryId
                category.db_modify_date = timezone.now()
                category.modifyUser = modifyUser
            
            category.save() 
            
        else:
            log.warning("Cannot modify new category. Category with same name already exits")
            return False
        return True
            
            
            
            
            
            
            
            
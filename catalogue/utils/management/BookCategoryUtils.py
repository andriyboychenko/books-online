from django.utils import timezone
from catalogue.models import BookCategory

class BookCategoryUtils:
    
    def removeCategory(self, bookCategoryId):
        bookCategory = BookCategory.objects.filter(id=bookCategoryId)
        
        if len(bookCategory) > 0:
            bookCategory[0].active = False
            bookCategory[0].save()
        else:
            print "Cannot remove new category. Category no more longger exists"
        
        
        
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
                    print "Cannot insert new category. Super category no more longger exists"

            category.save()
        else:
            print "Cannot insert new category. Category exits"
            

            
            
            
    def modifyCategory(self, bookCategoryId, bookCategoryName, bookCategoryDesc, superCategoryId, modifyUser):
        currentCategory = BookCategory.objects.filter(id = bookCategoryId, active = True)
        categoryWithSameName = BookCategory.objects.filter(category_name = bookCategoryName, active = True)
        
        canProceed = False
        if len(categoryWithSameName) == 0 and len(currentCategory) > 0:
            canProceed = True
        elif len(currentCategory) > 0:
            if currentCategory[0].id == categoryWithSameName[0].id:
                canProceed = True
                
        if canProceed:
            #User haven't selected super category
            if len(superCategoryId) == 0:
                currentCategory[0].category_name = bookCategoryName
                currentCategory[0].category_description = bookCategoryDesc
                currentCategory[0].db_modify_date = timezone.now()
                currentCategory[0].modifyUser = modifyUser
            else:
                currentCategory[0].category_name = bookCategoryName
                currentCategory[0].category_descriptio = bookCategoryDesc
                currentCategory[0].sub_category_of = superCategoryId
                currentCategory[0].db_modify_date = timezone.now()
                currentCategory[0].modifyUser = modifyUser
            
            currentCategory[0].save() 
            
        else:
            print "Cannot modify new category. Category exits"
            
            
            
            
            
            
            
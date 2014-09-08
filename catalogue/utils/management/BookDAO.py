import logging

from django.utils import timezone
from catalogue.entities.ResponseMessage import ResponseMessage
from catalogue.models import BookCategory, BookAttribute, BookAttributeType, BookItem, User

log = logging.getLogger("django")

class BookDAO:
    def removeBook(self, bookItemId, modifyUser):
        
        bookItem = BookItem.objects.filter(book_uuid=bookItemId)
        
        if len(bookItem) > 0:
            bookItem[0].active = False
            bookItem[0].modifyUser = modifyUser
            bookItem[0].save()
        else:
            log.warning("Cannot remove category. Category no more longger exists")
            return False
        return True

    
    def addNewBook(self, bookUUIDVal, bookName, bookAuthor, bookDesc, bookCategory, 
                   bookCover, bookQuality, bookLanguage, bookPrice, 
                   bookDiscount, bookNotable, bookImagesUrl, bookImagesNames, bookThumbnail, modifyUser):
        
        bookActiveCategory = BookCategory.objects.filter(id = bookCategory, active = True)
        bookActiveCover = BookAttribute.objects.filter(id = bookCover, active = True)
        bookActiveQuality = BookAttribute.objects.filter(id = bookQuality, active = True)
        bookActiveLanguage = BookAttribute.objects.filter(id = bookLanguage, active = True)
        
        if bookActiveCategory and bookActiveCover and bookActiveQuality and bookActiveLanguage:
            
            book = BookItem(
                  book_uuid = bookUUIDVal,
                  book_name = bookName,
                  book_author = bookAuthor,
                  book_description = bookDesc,
                  book_category = bookActiveCategory[0],
                  book_cover = bookActiveCover[0],
                  book_quality = bookActiveQuality[0],
                  book_language = bookActiveLanguage[0],
                  book_price = bookPrice,
                  book_discount = bookDiscount,
                  is_notable = bookNotable,
                  book_images_path = bookImagesUrl,
                  book_images_names = bookImagesNames,
                  book_thumbnail = bookThumbnail,
                  db_insert_date = timezone.now(), 
                  db_modify_date = timezone.now(), 
                  db_modify_user = modifyUser)
            book.save()
            return ResponseMessage(1, "success")
        
        else:    
            log.error("Something went wrong while was inserting book to database")
            return ResponseMessage(3, "error-inserting-to-database")
        
   
        
    def modifyBook(self, bookCategoryId, bookCategoryName, bookCategoryDesc, superCategoryId, modifyUser):
        print "----"


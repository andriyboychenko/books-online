import logging


import uuid
import StringIO
from PIL import Image, ImageOps
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json
from datetime import datetime
from django.conf import settings
from catalogue.entities import RU_ru
from catalogue.entities.ResponseMessage import ResponseMessage
from catalogue.models import User
from catalogue.utils.management.BookDAO import BookDAO
from catalogue.utils.management.BookImageUtils import BookImageUtils
from catalogue.models import BookItem

log = logging.getLogger("django")

def remove(request):
    object_id = request.POST["object_id"]
    action_response = {}
    
    try:
        users = User.objects.filter(id=1) #TODO: hardcoded
        
        if len(users) > 0:
            modifyUser = users[0]
                                    
            bookDAO = BookDAO()
            isRemoved = bookDAO.removeBook(object_id, True, modifyUser)
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


def insertBook(request):
    
    bookUUIDVal = str(uuid.uuid1())[:13]

    bookNameTxt = request.POST["book-name-txt"]
    bookAuthorTxt = request.POST["book-author-txt"]
    bookDescriptionTxt = request.POST["book-desc-txt"]
    
    bookCategorySelect = request.POST["category-select"]
    bookCoverSelect = request.POST["cover-select"]
    bookQualitySelect = request.POST["quality-select"]
    bookLanguageSelect = request.POST["language-select"]
    
    bookPriceTxt = request.POST["book-price-txt"]
    bookDiscountTxt = request.POST["book-discount-txt"]
    
    bookNotable = False
    if "book-is-with-priority" in request.POST.keys():
        bookNotable = True
    
    bookUploadedImages = request.FILES.getlist('file')
    
    bookId = request.POST["book-id"]
    
    
    status_code = 1 #1-ok, 2-warn, 3-error ---------------------
    
    resp = ResponseMessage(1,"success")

    try:
        
        bookImagesNames = []
        bookThumbnail = ""
        bookDynamicPath = ""
        imageCounter = 1
        currDate = datetime.today()
        
        for uploadedImage in bookUploadedImages:
            
            bookImageUtils = BookImageUtils(uploadedImage, currDate)
            
            if bookImageUtils.isValidFormat() :
                if bookImageUtils.isValidSize() :
                    
                    # Uploading image to the server
                    bookImageUtils.uploadImage()
                    
                    # When a new book is added with images, only the first image is defined as thumbnail. 
                    # Thumbnail can be chnaged in book item modification
                    if (imageCounter == 1):
                        bookImageUtils.generateThumnail()
                        bookThumbnail = bookImageUtils.imgNewNameThumb
                        bookDynamicPath = bookImageUtils.imageDynamicPath
                                                
                    # It's allowod to upload only 15 valid images per book
                    if imageCounter > settings.ALLOWED_IMAGE_QUANT:
                        resp = ResponseMessage(2, "wrong-image-quantity")
                        log.warning("Wrong image quantity! Only %d images are allowed. Other images will be discarded" % settings.ALLOWED_IMAGE_QUANT)
                        break;
                        
                    imageCounter += 1
                    bookImagesNames.append(bookImageUtils.imgName)
                     
                else:
                    resp = ResponseMessage(3,"wrong-image-size")
                    log.warning("Wrong image size! Only %d KB images are allowed. The image %s will be discarded" %
                                ((settings.ALLOWED_IMAGE_SIZE / 1024), bookImageUtils.imgOldName) )
            else: 
                resp = ResponseMessage(3,"wrong-image-format")
                log.warning("Wrong image size! Only JPG and PNG images are allowed. The image %s will be discarded" % (bookImageUtils.imgOldName) )
            
            
        # Inserting other book data only if image data is correct if it is exists
        if resp.getErrorCode() == 1 or not bookUploadedImages:
            
            users = User.objects.filter(id=1) #TODO: hardcoded
        
            if len(users) > 0:
                modifyUser = users[0]
                            
                bookDAO = BookDAO()
                
                # Modify book category
                if len(bookId) > 0:
                    print "tmp------------"
                    
                # Add new book category
                else:
                    resp = bookDAO.addNewBook(bookUUIDVal, bookNameTxt, bookAuthorTxt, bookDescriptionTxt, bookCategorySelect, 
                            bookCoverSelect, bookQualitySelect, bookLanguageSelect, bookPriceTxt, 
                            bookDiscountTxt, bookNotable, bookDynamicPath, bookImagesNames,
                            bookThumbnail, modifyUser)
                            
    except Exception as error:
        ResponseMessage(3,"internal-error")
        log.exception(error)
 
    
    bookItemList = BookItem.objects.filter(active=True).order_by('-db_insert_date')
    
        
    
    return render_to_response(
                              'catalogue/templates/book-management.html', 
                              {
                               'book_list': bookItemList, 
                               #'status': status_code,
                               'ResponseMessage': ResponseMessage,
                               'lang': RU_ru
                               })
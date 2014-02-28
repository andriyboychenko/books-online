import logging

from django.shortcuts import render_to_response
from django.conf import settings
from catalogue.entities import RU_ru


log = logging.getLogger("django")




def insertBook(request):

    bookNameTxt = request.POST["book-name-txt"]
    bookAuthorTxt = request.POST["book-author-txt"]
    bookDescriptionTxt = request.POST["book-desc-txt"]
    
    bookCategorySelect = request.POST["category-select"]
    bookCoverSelect = request.POST["cover-select"]
    bookQualitySelect = request.POST["quality-select"]
    bookLanguageSelect = request.POST["language-select"]
    
    bookPriceTxt = request.POST["book-price-txt"]
    bookDiscountTxt = request.POST["book-discount-txt"]
    
    bookIsPrioritized = False
    if "book-is-with-priority" in request.POST.keys():$
        bookIsPrioritized = True
    
    bookUploadedImages = request.FILES.getlist('file')
    
    status_code = 1 #1-ok, 2-warn, 3-error
    
    try:
    
        for uploadedImage in bookUploadedImages:
            if uploadedImage.content_type in settings.ALLOWED_IMAGE_UPLOAD:
                if uploadedImage._size < settings.ALLOWED_IMAGE_SIZE:
                    with open('/home/andriy/Pictures/books-test/'+str(uploadedImage), 'wb+') as destination:
                        for chunk in uploadedImage.chunks():
                            destination.write(chunk)
                else:
                    print "Wrong size!!"
            else: 
                print "Wrong format"
     
    except Exception as error:
        log.error(error)
        status_code = 3
        
    
    #book_category_id = request.POST["book-category-id"]
    
    
        
    
    return render_to_response(
                              'catalogue/templates/book-management.html', 
                              {
                               #'book_category_list': book_category_list, 
                               #'status': status_code,
                               'lang': RU_ru
                               })
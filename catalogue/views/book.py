import logging

from catalogue.entities import RU_ru

from .forms import UploadFileForm

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
    
    bookIsPrioritized = request.POST["book-is-with-priority"]
    
    print "bookIsPrioritized "+bookIsPrioritized
    
    #book_category_id = request.POST["book-category-id"]
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES['file']
            #https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
            #handle_uploaded_file(request.FILES['file'])
        
    
    return render_to_response(
                              'catalogue/templates/book-management.html', 
                              {
                               #'book_category_list': book_category_list, 
                               #'status': status_code,
                               'lang': RU_ru
                               })
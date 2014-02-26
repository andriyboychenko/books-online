from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('catalogue.views',
    url(r'^catalogue/$', 'common.index'),
    url(r'^catalogue/site-management/$', 'common.sitemanagement'),
    url(r'^catalogue/cover-management/$', 'common.covermanagement'),
    url(r'^catalogue/quality-management/$', 'common.qualitymanagement'),
    url(r'^catalogue/language-management/$', 'common.languagemanagement'),
    url(r'^catalogue/book-management/$', 'common.bookmanagement'),
    url(r'^catalogue/insert-book-category/$', 'category.insert_book_category'),
    url(r'^catalogue/insert-book-attribute/$', 'bookattribute.insertBookAttribute'),
    url(r'^catalogue/insert-book/$', 'book.insertBook'),
    
    url(r'^catalogue/(?P<book_id>\d+)/$', 'bookdetail'),

    
    
    
    #AJAX
    url(r'^ajax-catalogue/bookcategory/remove/$',               'category.remove'),
    url(r'^ajax-catalogue/bookattribute/remove/$',              'bookattribute.remove'),
    url(r'^ajax-catalogue/bookcategory/edit-load-data/$',       'category.edit_load_data'),
    url(r'^ajax-catalogue/bookattribute/edit-load-data/$',      'bookattribute.loadEditData'),
    url(r'^ajax-catalogue/bookcategory/valid-name/$',           'category.valid_name'),
    url(r'^ajax-catalogue/bookattribute/valid-name/$',          'bookattribute.validName'),
    
    
    
    # Examples:
    # url(r'^$', 'books_online.views.home', name='home'),
    # url(r'^books_online/', include('books_online.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from django.urls import path
from .views import main_page,flogin_page,ilogin_page,dlogin_page,logoutuser,farmer_page,industry_page,da_page,update_quantity,feedback,generate_payment,confirm_payment,chatbot
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',main_page,name="Main Page"),
    path('flogin/',flogin_page,name="Flogin Page"),
    path('ilogin/',ilogin_page,name="Ilogin Page"),
    path('dlogin/',dlogin_page,name="Dlogin Page"),
    path('logout/',logoutuser,name='logout'),
    path('farmer/',farmer_page,name="Farmer Page"),
    path('industry/',industry_page,name="Industry Page"),
    path('update-quantity/', update_quantity, name='update_quantity'),
    path('da/',da_page,name="DA Page"),
    path('feedback/',feedback,name="Feedback"),
    path('generate-payment/', generate_payment, name='generate_payment'),
    path('confirm-payment/', confirm_payment, name='confirm_payment'),
    path('chat/', chatbot, name="chatbot"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
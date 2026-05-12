from django.urls import path

from .views import ParagraphCreateView, SearchWordView


urlpatterns = [

    path('create/', ParagraphCreateView.as_view(), name='create-paragraph'),

    path('search/', SearchWordView.as_view(), name='search-word'),

]

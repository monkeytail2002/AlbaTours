from django.urls import path
#Import views
from .views import newsletter_signup, newsletter_unsubscribe, report, create_newsletter, newsletter_list, newsletter_detail, newsletter_edit, newsletter_delete, occupancy_report, sailing_report, boarding_report

#Set up the URL patterns
urlpatterns = [
    path('subscribe/', newsletter_signup, name="subscribe"),
    path('unsubscribe/', newsletter_unsubscribe, name ="unsubscribe"),
    path('reports/', report, name ="reports"),
    path('newsletter/', create_newsletter, name='newsletter'),
    path('dashboard/', newsletter_list, name='dashboard'),
    path('detail/<int:pk>', newsletter_detail, name="detail"),
    path('edit/<int:pk>', newsletter_edit, name="edit"),
    path('newsletterdelete/<int:pk>', newsletter_delete, name="delete"),
    path('occupancy/', occupancy_report, name="occupancy"),
    path('sailing/', sailing_report, name="sailing"),
    path('boarding/', boarding_report, name="boarding"),
      
]


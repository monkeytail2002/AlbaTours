from django.contrib import admin
from .models import NewsletterCustomer, Newsletter
# Register your models here.

#Sets up the newsletter side on administration panel
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added',)
    
    
admin.site.register(NewsletterCustomer, NewsletterAdmin)


admin.site.register(Newsletter)

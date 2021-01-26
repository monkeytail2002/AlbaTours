from django.db import models

# Create your models here.

#Model to track subscribers to newsletter
class NewsletterCustomer(models.Model):
    email = models.EmailField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

#Model to track/create newsletter
class Newsletter(models.Model):
    EMAILSTATUS_CHOICES = [('Draft','Draft'),('Published', 'Published')]
    
    subject = models.CharField(max_length = 250)
    body = models.TextField()
    email = models.ManyToManyField(NewsletterCustomer)
    status = models.CharField(max_length=10, choices=EMAILSTATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    



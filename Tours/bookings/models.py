from django.db import models

# Create your models here.

class Prices(models.Model):
    depart = models.CharField(max_length=6)
    island = models.CharField(max_length=6, null=True)
    fare = models.CharField(max_length=7)
    price = models.DecimalField(decimal_places=2, max_digits=6)
        
    def __str__(self):
        return self.depart
    
#island model/table
class Routes(models.Model):
    sailing_route = models.CharField(max_length=30,null=True)
    occupancy = models.IntegerField(null=True)
    wheelchair = models.CharField(max_length=1,default="0",null=True)
    sailing_date = models.DateField(auto_now=False,null=True)
    sailing_day = models.CharField(max_length=30,null=True)
    max_fweight = models.DecimalField(decimal_places=0, max_digits=8)
    rem_fweight = models.DecimalField(decimal_places=0, max_digits=8)
    
    
    def __str__(self):
        return self.island_name

    
class Booked(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'
    
    TICKET_STATUSES = ((BOOKED, 'Booked'), (CANCELLED, 'Cancelled'))
    user_id = models.IntegerField(null=True)
    booked_route = models.CharField(max_length=30, null=True)
    booked_seats = models.IntegerField(null=True)
    booked_date = models.DateField(auto_now=False, null=True)
    pname = models.CharField(max_length=255)
    time = models.CharField(max_length=2, null=True)
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=255)
    wheelchair_needed = models.CharField(max_length=1,default="0",null=True)
    adults = models.IntegerField(null=True)
    children = models.IntegerField(null=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    
    
    def __str__(self):
        return self.pname

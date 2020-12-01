from django import forms
from tempus_dominus.widgets import DatePicker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
    
#Form for booking tickets
class BookingForm(forms.Form):
    INTEGER_CHOICES = [tuple([x,x]) for x in range(1,31)]
    FERRY_CHOICES = [('1', 'Morar - Eigg'), ('2', 'Morar - Muck'), ('3', 'Morar - Rum'), ('4', 'Eigg - Muck'), ('5', 'Eigg - Rum')]
    WHEELCHAIR_CHOICES = [('no','No'),('yes', 'Yes')]
   

    ferry_date = forms.DateField(widget=DatePicker(), initial='2021-05-20')
    return_route = forms.IntegerField(label="Route", widget=forms.Select(choices=FERRY_CHOICES))
    no_seats = forms.IntegerField(label="Number of seats", widget=forms.Select(choices=INTEGER_CHOICES))
    pname = forms.CharField(label="Passenger name to book under", max_length = 255)
    wheelchair = forms.CharField(label="Is wheelchair space required?", max_length= 3, required=False, widget=forms.Select(choices=WHEELCHAIR_CHOICES))
    adults = forms.IntegerField(label="Number of adults")
    child_baby = forms.IntegerField(label="Any children 2 years and under?")
    child_child = forms.IntegerField(label="Any children aged 3-10 years old?")
    child_teen = forms.IntegerField(label="Any children aged 11-16 years old?")
    
    
    
class UserRegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=255)
    full_name = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ("username","full_name", "email", "password1", "password2", "phone_number")
        
    def save(self, commit=True):
        user = super(UserRegForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned.data["full_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
        
from django import forms
from tempus_dominus.widgets import DatePicker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Booked

    
    
#Form for booking tickets
class BookingForm(forms.Form):
    INTEGER_CHOICES = [tuple([x,x]) for x in range(1,31)]
    SEAT_CHOICES = [tuple([x,x]) for x in range(0,31)]
    FERRY_CHOICES = [('-','---'),('1', 'Morar - Eigg'), ('2', 'Morar - Muck'), ('3', 'Morar - Rum'), ('4', 'Eigg - Muck'), ('5', 'Eigg - Rum')]
    WHEELCHAIR_CHOICES = [('-','---'),('no','No'),('yes', 'Yes')]
   

    ferry_date = forms.DateField(widget=DatePicker(options={'minDate':'2021-05-20', 'maxDate':'2021-10-21',},), initial='2021-05-20')
    return_route = forms.IntegerField(label="Route", widget=forms.Select(choices=FERRY_CHOICES))
    no_seats = forms.IntegerField(label="Number of seats", widget=forms.Select(choices=INTEGER_CHOICES))
    pname = forms.CharField(label="Passenger name to book under", max_length = 255)
    wheelchair = forms.CharField(label="Is wheelchair space required?", max_length= 3, required=False, widget=forms.Select(choices=WHEELCHAIR_CHOICES))
    adults = forms.IntegerField(label="Number of adults", widget=forms.Select(choices=SEAT_CHOICES))
    child_baby = forms.IntegerField(label="Any children 2 years and under?",widget=forms.Select(choices=SEAT_CHOICES))
    child_child = forms.IntegerField(label="Any children aged 3-10 years old?",widget=forms.Select(choices=SEAT_CHOICES))
    child_teen = forms.IntegerField(label="Any children aged 11-16 years old?",widget=forms.Select(choices=SEAT_CHOICES))
    
    
    
class UserRegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email", "password1", "password2", "phone_number")
        
    def save(self, commit=True):
        user = super(UserRegForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
        
class ContactForm(forms.Form):
    first_name = forms.CharField(label="What is your first name?", max_length = 255)
    last_name = forms.CharField(label="What is your last name?",max_length=255)
    email_address = forms.EmailField(label="Please enter your email address",max_length=255)
    message = forms.CharField(label="What is your message?", widget=forms.Textarea)
    
    
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']

        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False,max_length=255)
    first_name = forms.CharField(required=False,max_length=255)
    last_name = forms.CharField(required=False,max_length=255)
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name", "email", "phone_number"]
        
        
class EditForm(forms.Form):
    WHEELCHAIR_CHOICES = [('no','No'),('yes', 'Yes')]
    EDIT_CHOICES = [('more','More seats'),('less', 'Less seats')]
    INTEGER_CHOICES = [tuple([x,x]) for x in range(1,31)]
    WHEELCHAIRSPACE_CHOICES = [('no','No'),('yes', 'Yes')]
    SEAT_CHOICES = [tuple([x,x]) for x in range(0,31)]

    
    
    ticket_ref = forms.IntegerField(required=True)
    ferry_date = forms.DateField(required=True, widget=DatePicker(options={'minDate':'2021-05-20', 'maxDate':'2021-10-21',},), initial='2021-05-20')
    edit_seats = forms.CharField(label="More or less seats?", max_length= 4, required=True, widget=forms.Select(choices=EDIT_CHOICES))
    no_seats = forms.IntegerField(label="How many seats will you need overall, including the current amount?", widget=forms.Select(choices=INTEGER_CHOICES))
    wheelchair_space = forms.CharField(label="Do you need an extra wheelchair space?", max_length= 3, required=True, widget=forms.Select(choices=WHEELCHAIRSPACE_CHOICES))
    wheelchair = forms.CharField(label="Have you already booked a wheelchair space?", max_length= 3, required=True, widget=forms.Select(choices=WHEELCHAIR_CHOICES))
    wheelchair_req = forms.CharField(label="Do you still require a wheelchair space if you already booked one?", max_length= 3, required=True, widget=forms.Select(choices=WHEELCHAIRSPACE_CHOICES))
    adults = forms.IntegerField(label="Number of adults travelling, including those currently booked?", widget=forms.Select(choices=SEAT_CHOICES), required=True)
    child_baby = forms.IntegerField(label="Any children 2 years and under, including those currently booked?", widget=forms.Select(choices=SEAT_CHOICES),required=True)
    child_child = forms.IntegerField(label="Any children aged 3-10 years old, including those currently booked?", widget=forms.Select(choices=SEAT_CHOICES), required=True)
    child_teen = forms.IntegerField(label="Any children aged 11-16 years old, including those currently booked?", widget=forms.Select(choices=SEAT_CHOICES), required=True)

        
class CancelForm(forms.ModelForm):
    ticket_ref = forms.IntegerField()
    
    
    class Meta:
        model = Booked
        fields = ["ticket_ref"]
    
class CeilidhForm(forms.ModelForm):
        
        confirm = forms.BooleanField(label="Will ye bide your time wi us?",required=False)
        partner_name = forms.CharField(label="Who will be your dancing partner?", max_length = 255, required = False)
    
    
        class Meta:
            model = Profile
            fields = ['confirm', 'partner_name']


    


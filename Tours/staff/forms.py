from django import forms
#Import models
from .models import NewsletterCustomer, Newsletter
#Import date picker form tempus dominus
from tempus_dominus.widgets import DatePicker

#Sets the sign up form for the newsletter
class NewsletterCustomerSignUpForm(forms.ModelForm):
    #Sets the meta and fields for the form.
    class Meta:
        model = NewsletterCustomer
        fields = ['email']
        
        #Ensures that the user input isn't an injection
        def clean_email(self):
            email = self.cleaned_data.get('email')
            
            return email
    
#Sets the creation form for the newsletter
class NewsletterCreationForm(forms.ModelForm):
    #Sets the meta class and fields
    class Meta:
        model = Newsletter
        fields = (
            'subject','body','email', 'status'
        )
        
        
        
#Sets the form for the reports by date            
class SailingReportForm(forms.Form):
    #Sets the date picker
    report_date = forms.DateField(widget=DatePicker(), initial='2021-05-20', required=False) 

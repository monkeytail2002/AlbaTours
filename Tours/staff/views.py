#Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#Django.contrib based imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages

#Django.core based imports
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Model imports
from .models import NewsletterCustomer, Newsletter
from bookings.models import Routes, Booked

#Form imports
from .forms import NewsletterCustomerSignUpForm, SailingReportForm, NewsletterCreationForm


#Set up the signup process for the newsletter
def newsletter_signup(request):
   #Checks if the method from the page is a POST or GET
    if request.method == 'POST':
            
        form = NewsletterCustomerSignUpForm(request.POST)
        #Checks the csrf token
        if form.is_valid():          
            instance = form.save(commit=False)
            #Checks to see if the email address is already entered in the database
            if NewsletterCustomer.objects.filter(email=instance.email).exists():
                form = NewsletterCustomerSignUpForm
                messages.warning(request,
                                 f"This email address already exists as a subscriber.",
                                 "alert alert-warning alert-dismissable fade show")
                return render(request, 'newsletters/newsletter_signup.html', {'form':form})
            else:
                instance.save()
                messages.success(request,
                                 f"Newsletter subscription successful.",
                                 "alert alert-success alert-dismissable")
                return render(request, 'newsletters/newsletter_signup.html', {'form':form})
    else:
 
        template = 'newsletters/newsletter_signup.html'
        
        form = NewsletterCustomerSignUpForm
        
        return render(request, template, {'form':form})


#Setit so that people can unsubscribe
def newsletter_unsubscribe(request):
    #Checks if the method from the page is a POST or GET
    if request.method == 'POST':
        form = NewsletterCustomerSignUpForm(request.POST)
        #Checks the csrf token
        if form.is_valid():
      
            instance = form.save(commit=False)
        #Checks for an email address in the database and deletes it if it exists
            if NewsletterCustomer.objects.filter(email=instance.email).exists():
                test = NewsletterCustomer.objects.get(email=instance.email)
                if test:
                    test.delete()
            messages.success(request,
                                 f"Unsubscribed from the newsletter.",
                                 "alert alert-success alert-dismissable fade show")    
            return render(request, 'newsletters/newsletter_unsubscribe.html', {'form':form})
        else:
            messages.warning(request,
                                 f"We could not find your email address.",
                                 "alert alert-warning alert-dismissable fade show")
            return render(request, 'newsletters/newsletter_unsubscribe.html', {'form':form})
    else:
        form = NewsletterCustomerSignUpForm
        context = {
            'form': form,
            
        }
        
        template = 'newsletters/newsletter_unsubscribe.html'
        
        return render(request, template, context)




#function to create newsletter and send it
@login_required(login_url='login')
def create_newsletter(request):
    print(f'{request.method}create newsletter')
    #Checks for POST or GET
    if request.method == "POST":
        form = NewsletterCreationForm(request.POST)
        #Check form is valid
        if form.is_valid():
            instance = form.save()
            newsletter = Newsletter.objects.get(id=instance.id)
            #Checks to see if the newsletter is a draft or if it's published
            if newsletter.status == "Published":
                subject = newsletter.subject
                body = newsletter.body
                from_email = "theonlyscotiaislandcruisesglencross@gmail.com"
                #Sends email to selected emails.
                for email in newsletter.email.all():
                    try:
                        send_mail(subject, body, from_email,recipient_list=[email.email], fail_silently=True)
                        messages.success(request,f"Email sent", "alert alert-success alert-dismissable fade show")                        
                    except BadHeaderError:
                        messages.error(request,f"Apologies but we were unable to send the email.  Please try again", "alert alert-error alert-dismissable fade show")
                        return HttpResponse('Invalid header found') 
                    context = {
                        'form': form,
                    }
                    return render(request, 'controlpanel/control_newsletter.html', context)
            else:
                form = NewsletterCreationForm
                context = {
                    'form': form,
                }
                messages.success(request,f"Draft saved.", "alert alert-success alert-dismissable fade show")
                return render(request, 'controlpanel/control_newsletter.html', context)
        else:
            messages.error(request,f"Apologies but there was an issue with the form.  Please contact an administrator.", "alert alert-error alert-dismissable fade show")
            form = NewsletterCreationForm
            context = {
                'form': form,
            }
            
            template = 'controlpanel/control_newsletter.html'
            return render(request, template, context)
    else:
        form = NewsletterCreationForm
        context = {
            'form':form,
        }
        template = 'controlpanel/control_newsletter.html'
        return render(request, template, context)
    
    
    

    #List of newsletters on dashboard
@login_required(login_url='login')               
def newsletter_list(request):
    print(f'{request.method}newspaper list')
    newsletters = Newsletter.objects.all()
    #Set paginator to 10 newsletters per page
    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    #Set the index for the pages.
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index -5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    

    context = {
        'items': items,
        'page_range': page_range
    }
    
    template = 'controlpanel/dashboard.html'
    
    return render(request, template, context)
    

#Make a detailed view of the newsletter.
@login_required(login_url='login')
def newsletter_detail(request, pk):
    print(f'{request.method}detail newsletter')
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    context = {
        'newsletter': newsletter        
    }
    
    template = 'controlpanel/detail.html'
    
    return render(request, template, context)
                  

    #Creates edit for newsletter
@login_required(login_url='login')    
def newsletter_edit(request, pk):
    print(f'{request.method}edit newsletter')
    newsletter = get_object_or_404(Newsletter, pk=pk)
    #Checks for POST or GET
    if request.method == "POST":
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        #Checks the csrf token for validity
        if form.is_valid():
            newsletter = form.save()
            messages.success(request,f"Edit saved", "alert alert-success alert-dismissable fade show") 
            if newsletter.status == "Published":
                subject = newsletter.subject
                body = newsletter.body
                from_email = "theonlyscotiaislandcruisesglencross@gmail.com"
                #if status is published then an email is sent to the selected email addresses
                for email in newsletter.email.all():
                    try:
                        send_mail(subject, body, from_email,recipient_list=[email.email], fail_silently=True)
                        messages.success(request,f"Newsletter sent out", "alert alert-success alert-dismissable fade show")                        
                    except BadHeaderError:
                        messages.error(request,f"Apologies but we were unable to send the email.  Please try again", "alert alert-error alert-dismissable fade show")
                        return HttpResponse('Invalid header found') 
            
                context = {
                    'newsletter': newsletter        
                }
                template = 'controlpanel/detail.html'
                return render(request, template, context)
        
            else:
                #Saves the draft
                newsletter = form.save()
                messages.success(request,f"Draft saved", "alert alert-success alert-dismissable fade show") 
                context = {
                    'newsletter': newsletter        
                }
                template = 'controlpanel/detail.html'
                return render(request, template, context)
        else:
            form = NewsletterCreationForm
            context = {
                'form':form,
            }
            template = 'controlpanel/control_newsletter.html'
            messages.error(request,f"There was an issue with the website form.  Please contact an administrator.", "alert alert-error alert-dismissable fade show") 
            return render(request, template, context)
    

    else:
        form = NewsletterCreationForm(instance=newsletter)
        context = {
            'form':form,
        }
        template = 'controlpanel/control_newsletter.html'
        return render(request, template, context)
    

 #Function to delete newsletters  
@login_required(login_url='login')
def newsletter_delete(request, pk):
    print(f'{request.method}newsletter delete')
    newsletter = get_object_or_404(Newsletter, pk=pk)
    #Checks for POST or GET
    if request.method == "POST":
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        #Checks csrf token
        if form.is_valid():
            newsletter.delete()
            newsletters = Newsletter.objects.all()
            #Sets pages to 10 newsletters per page
            paginator = Paginator(newsletters, 10)
            page = request.GET.get('page')
            
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
            #Sets page range        
            index = items.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index -5 else max_index
            page_range = paginator.page_range[start_index:end_index]
            
            context = {
                'items': items,
                'page_range': page_range
            }
            
            template = 'controlpanel/dashboard.html'
            messages.success(request,f"Newsletter deleted.", "alert alert-success alert-dismissable fade show") 
            return render(request, template, context)
        else:
            messages.error(request,f"There was an issue with the website form.  Please contact an administrator.", "alert alert-success alert-dismissable fade show") 
            newsletters = Newsletter.objects.all()
            
            paginator = Paginator(newsletters, 10)
            page = request.GET.get('page')
            
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
                    
            index = items.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index -5 else max_index
            page_range = paginator.page_range[start_index:end_index]
            
            context = {
                'items': items,
                'page_range': page_range
            }
            
            template = 'controlpanel/dashboard.html'
            return render(request, template, context)
    else:
        form = NewsletterCreationForm(instance=newsletter)
        
        context = {
                    'form': form,     
                }
        template = 'controlpanel/newsletter_delete.html'
        
        return render(request, template, context)
            

   

 
#Sets the main report page                
@login_required(login_url='login')    
def report(request):
    print(f'{request.method}staff report')
    return render(request, 'staff/reports.html')

#  sets the occupancy report
@login_required(login_url='login')
def occupancy_report(request):
    print(f'{request.method}report occupancy')
    occupancy = Routes.objects.all()
    
    
   
    #sets the paginator to 10 rows per page
    paginator = Paginator(occupancy, 10)
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    #sets the page range
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index -5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    

    context = {
        'items': items,
        'page_range': page_range
    }
   
    template = 'staff/occupancy.html'
    
    return render(request, template, context)


#Produces the sailing report
@login_required(login_url='login')
def sailing_report(request):
    print(f'{request.method}report sailing')
    #Checks for POST or GET
    if request.method== "POST":
        s_form = SailingReportForm(request.POST)
        #Checks csrf token
        if s_form.is_valid():
            report_date = request.POST.get('report_date')
            items = Routes.objects.filter(sailing_date = report_date)
            context = {
                's_form':s_form,
                'items':items,
            }
            return render(request, 'staff/sailingroute.html', context)
        else:
            messages.error(request,
                                 f"There was an issue generating the report.  Please report this to a web admin.",
                                 "alert alert-error alert-dismissable fade show")
            return redirect('reports')
    else:
        s_form = SailingReportForm
        context = {
            's_form':s_form,
        }
        return render(request, 'staff/sailingroute.html', context)
    
    
#Creates boarding report    
@login_required(login_url='login')
def boarding_report(request):
    print(f'{request.method}report boarding')
    #checks for POST or GET
    if request.method == "POST":
        b_form = SailingReportForm(request.POST)
        report_date = request.POST.get('report_date')
        #Checks csrf token
        if b_form.is_valid():
            boarding = Booked.objects.filter(booked_date = report_date)   
            #Sets number of rows to 10 per page
            paginator = Paginator(boarding, 10)
            page = request.GET.get('page')
            
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
            #Sets the page range    
            index = items.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index -5 else max_index
            page_range = paginator.page_range[start_index:end_index]
            
            context = {
                'items': items,
                'page_range': page_range,
                'b_form':b_form,
            }
            template = 'staff/boardingreport.html'
            
            return render(request, template, context)
        else:
            messages.error(request,f"There was an issue with the website form.  Please contact an administrator.", "alert alert-success alert-dismissable fade show") 
            b_form = SailingReportForm    
            context = {
                'b_form':b_form,
            }
            template = 'staff/boardingreport.html'
            
            return render(request, template, context)
    else:
        b_form = SailingReportForm  
        
        context = {
            'b_form':b_form,
        }
        template = 'staff/boardingreport.html'
        return render(request, template, context)

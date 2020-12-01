from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Routes, Booked, Prices
from .forms import BookingForm, UserRegForm
from decimal import Decimal




# Create your views here.
def home(request):
    return render(request, 'bookings/home.html')

def island(request):
    return render(request = request,
                 template_name='bookings/islands.html')


#def bookrum(request):
#     return render(request = request,
#                 template_name='bookings/bookrum.html',
#                 context = {"islands":Islands.objects.filter(island_name="Rum").values(), 'form':form})

#def bookmuck(request):
#    return render(request = request,
#                  template_name='bookings/bookmuck.html',
#                  context = {"islands":Islands.objects.filter(island_name="Muck").values(), 'form':form})
    
#def bookeigg(request):
#    form = BookingForm()
#    return render(request = request,
#                  template_name='bookings/bookeigg.html',
#                  context = {'islands':Islands.objects.filter(island_name="Eigg").values(), 'form':form})



def bookferry(request):
    form = BookingForm()
    return render(request = request,
                  template_name='bookings/bookferry.html',
                  context = {'prices':Prices.objects.all(),'form':form})


#view for booking system
#@login_required(login_url='login')
def bookings(request):
    context={}
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            #take in form details and information from tables
            ferry_date = form.data.get('ferry_date')
            return_route = form.data.get('return_route')
            seats_r = int(form.data.get('no_seats'))
            pname_r = form.data.get('pname')
            route = Routes.objects.get(sailing_date = ferry_date)
            wheel = form.data.get('wheelchair')
            adults = int(form.data.get('adults'))
            baby = int(form.data.get('child_baby'))
            child = int(form.data.get('child_child'))
            teen = int(form.data.get('child_teen'))
            child_p = Prices.objects.get(id=7)
            teen_p = Prices.objects.get(id=8)
            
             #Checks to see what price the adult ticket should be   
            if return_route == "1":
                adult = Prices.objects.get(id=return_route)
            elif return_route == "2":
                adult = Prices.objects.get(id=return_route)
            elif return_route == "3":
                adult = Prices.objects.get(id=return_route)   
            elif return_route == "4":
                adult = Prices.objects.get(id=return_route)
            else:
                adult = Prices.objects.get(id=return_route)
            #Checks to see if there is an entry in the Routes table that is valid
            if route:
                #Checks for wheelchair ticket
                if wheel == "yes":
                    wheel = "1"
                    if route.wheelchair == "0":
                        if route.occupancy > int(seats_r):
                            ferry = route.sailing_route
                            priced_route = Prices.objects.get(id=return_route)
                            priced_route = priced_route.island
                            seats_left = route.occupancy
                            child_c = int(child) * child_p.price
                            teen_c = int(teen) * teen_p.price
                            adult_c = int(adults) * adult.price
                            total_cost = child_c + teen_c + adult_c
                            children = child + baby + teen
                            userid_a = 2 #request.user.id
                            rem = route.occupancy - seats_r
                            Routes.objects.filter(sailing_date=ferry_date).update(occupancy=rem, wheelchair="1") #Updates remaining tickets available and wheelchair value
                            #Creates and entry in the Booked table
                            book = Booked.objects.create(pname=pname_r, user_id=userid_a, time = '11:00', booked_seats = seats_r, booked_date=ferry_date, booked_route = priced_route, wheelchair_needed = wheel, adults = adults, children = children,status='BOOKED', total_cost = total_cost)
                            print('--------------------- Booking id ---------------------', book.id)
                            #Renders the booking ticket receipt with variable information
                            return render(request, 'bookings/booked.html', locals())
                        else:
                            print(1) #Allows me to identify where an error appears by printing to console
                            context["error"] = "Sorry, only { seats_left } seats remaining"
                            return render(request, 'bookings/home.html')
                    else:
                        print(2) #Allows me to identify where an error appears by printing to console
                        context["error"] = "Sorry, but we have no wheelchair capable spaces left on the ferry."
                        return render(request, 'bookings/home.html')
                else:
                    #As above with no wheelchair entry
                    wheel="0"
                    if route.occupancy > int(seats_r):
                            ferry = route.sailing_route
                            priced_route = Prices.objects.get(id=return_route)
                            priced_route = priced_route.island
                            seats_left = route.occupancy
                            child_c = child * child_p.price
                            teen_c = teen * teen_p.price
                            adult_c = adults * adult.price
                            total_cost = child_c + teen_c + adult_c
                            children = child + baby + teen
                            userid_a = request.user.id
                            rem = route.occupancy - seats_r
                            Routes.objects.filter(sailing_date=ferry_date).update(occupancy=rem, wheelchair=True) #Updates remaining tickets available
                            book = Booked.objects.create(pname=pname_r, user_id=userid_a, time = '11:00', booked_seats = seats_r, booked_date=ferry_date, booked_route = priced_route, wheelchair_needed = wheel, adults = adults, children = children,status='BOOKED', total_cost = total_cost)
                            print('--------------------- Booking id ---------------------', book.id)
                            return render(request, 'bookings/booked.html', locals())
                    else:
                        print(3) #Allows me to identify where an error appears by printing to console
                        context["error"] = "Sorry, only { seats_left } seats remaining"
                        return render(request, 'bookings/home.html')
            else:
                print(4) #Allows me to identify where an error appears by printing to console
                context["error"] = "Sorry, but the ferry does not run to this island on that day."
                return render(request, 'bookings/home.html')
        else:
            print(5) #Allows me to identify where an error appears by printing to console
            context["error"] = "Sorry, there was an issue with our booking system.  Please try again later"                               
            return render(request, 'bookings/home.html')
    

        
def register(request):
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return render(request, 'bookings/home.html')
        
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "bookings/register.html",
                          context={"form":form})

    form = UserRegForm
    return render(request = request,
                  template_name = "bookings/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    return render(request, 'bookings/home.html')



def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "bookings/login.html",
                    context={"form":form})
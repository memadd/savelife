import datetime
from datetime import datetime, date, timedelta 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from . models import Stock
from . choices import city_choices, blood_choices


# date difference
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def register(request):
    context = {
        'city_choices': city_choices,
        'blood_choices': blood_choices
    }
    if request.method == 'POST':
        if not request.POST.get('city') and not request.POST.get('virus') and not request.POST.get('type'):
            messages.error(request, 'please fill the form properly.')
            return render (request, 'donors/register.html', context)
        if not request.POST['last'] and not request.POST['national']:
            messages.error(request, 'please fill the form properly.')
            return render (request, 'donors/register.html', context)
        #Get form values
        name = request.POST['name']
        email = request.POST['email']
        national_id = request.POST['national']
        last_donated = request.POST['last']
        city = request.POST['city']
        blood_type = request.POST['type']
        virus_test = request.POST['virus']

        if virus_test == 'positive':
            send_mail(
            'SaveLife Blood Donation Inform',
            'Hello ' +name+ '. Your blood test virus is positive, we are sorry you can\'t donate unitl it is negative',
            'messieo.104@gmail.com',
            [email],
            fail_silently=False,
            )
            messages.success(request, 'Thanks for registeration we will get to you soon.')
            return redirect('index')
        else:
            #calculate days from last donation
            today = str(date.today())
            days = days_between(today, last_donated)
            donate_after = 90 - days
            if days < 90:
                send_mail(
                'SaveLife Blood Donation Inform',
                'Hello ' +name+ '. You could be able to donate after ' +str(donate_after)+ ' days.',
                'messieo.104@gmail.com',
                [email],
                fail_silently=False,
                )

                messages.success(request, 'Thanks for registeration we will get to you soon.')
                return redirect('index')

            else:
                today = date.today()
                exp = today + timedelta(days=42)
                exp_date = str(exp)
                stock = Stock(city=city, blood_type=blood_type, exp_date=exp_date)
                stock.save()
                messages.success(request, 'Thanks for registeration we will get to you soon.')
                return redirect('index')
        
        
    
    else:
        return render (request, 'donors/register.html', context)

    


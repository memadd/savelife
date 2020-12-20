from django.shortcuts import render
from django.contrib import messages
from . choices import status_choices
from donors.choices import blood_choices, city_choices
from donors.models import Stock

def hospital(request):
    context = {
        'city_choices': city_choices,
        'blood_choices': blood_choices,
        'status_choices': status_choices
    }
    if request.method == 'POST':
        if not request.POST.get('city') and not request.POST.get('type'):
            messages.error(request, 'please fill the form first')
            return render(request, 'hospitals/request.html', context)
        city = request.POST['city']
        blood_type = request.POST['type']
        patient_status = request.POST['status']

        query_list = Stock.objects.filter(city__iexact=city)
        if query_list:
            query_list=query_list.filter(blood_type__iexact=blood_type)
            query_list.delete()
            messages.success(request,'this blood exist in your city\'s bank we will send it immediately')
            return render(request, 'hospitals/request.html', context)
        else:
            messages.error(request,'your city\'s bank doesn\'t have this blood type')
            return render(request, 'hospitals/request.html', context)
        
            
      
    else:
        return render(request, 'hospitals/request.html', context)

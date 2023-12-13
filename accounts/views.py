from django.shortcuts import render,  redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from prep_app.models import UserFacilityAssignment
from django.db.models import Q
from django.contrib.auth.models import User

def login_user(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        facility1 = request.POST['facility']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            query = Q(user=user) & Q(facility=facility1)
            results = UserFacilityAssignment.objects.filter(query)

            if results.exists():
                request.session['facility'] = facility1
                request.session['User'] = username
                user1 = User.objects.get(username=user)
                user_id = user1.id
                request.session['User_id'] = user_id

               

                #login(request, user)
                return redirect ('client_list')
            else:
                messages.success(request,'Username or password or site selected is incorrect')
                return redirect ('login_user')
        else:
            messages.success(request,'Username or password or site selected is incorrect')
            return redirect ('login_user')    
            
    return render(request, 'authentication\login.html')

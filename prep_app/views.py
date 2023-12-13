
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, AddressForm, ARVMedicationForm, CD4CountForm, ViralLoadForm, PhysicalExamForm,  PrepStatusDetailForm, SocialForm, RiskForm, EmergencyContactForm, STI_TestsDoneForm, RiskAssessmentForm, PrepEligibilityForm, SexualHistoryForm, DocketNewForm, OutOfCareStatusForm, Liver_Kidney_TestsForm
from .models import Client, Address, ARVMedication, CD4Count, ViralLoad, PhysicalExam,  PrepStatusDetail, SocialHistory, RiskHistory, EmergencyContact, STI_TestsDone, RiskAssessment, PrepEligibility, SexualHistory, Facility, CommunityCode, Docket_new, OutOfCareStatus, Liver_Kidney_Tests
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required



def close_window(request):
    return render(request, 'close_window.html')


def reports1(request):
    return render(request, 'reports1.html')


#@login_required(login_url='/accounts/login_user/')
def client_list(request):
    facilityname = ''
    facility_id1 = request.session['facility']
    try:
        facilityname = Facility.objects.get(pk=facility_id1)
    except Facility.DoesNotExist:
        facilityname = None

    words = ''
    query_search = request.GET.get('query')
    
    myclients1 = Client.objects.filter(last_name__icontains='x87oxq123')
    mycs = Client.objects.prefetch_related('docket_new_set').all()

    if query_search:
        words = query_search.split()

        query = Q()
        for word in words:
            query &= Q(last_name__icontains=word) | Q(first_name__icontains=word) | Q(middle_name__icontains=word) | Q(pet_name__icontains=word)  | Q(docket_new__docket_no__icontains=word) | Q(unique_identfier_code__icontains=word)
        
        myclients = mycs.filter(query).order_by('last_name', 'first_name').distinct()
        

    else:
        myclients = mycs.filter(last_name='zs456&^$g34@#')

    return render(request, 'client_list.html', {'clients': myclients, 'facilityname': facilityname})

#-------------------

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by_id = request.session['User_id']
            client.facility_id = request.session['facility']
            client = form.save()
            return redirect('edit_client', client_id=client.id)
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})


def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('edit_client', client_id=client_id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form, 'client': client, 'client_id': client_id})


def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'delete_client.html', {'client': client})

def fetch_communities(request):
    parish_id = request.GET.get('parish_id')
    print(f"Received parish_id: {parish_id}")
    communities = CommunityCode.objects.filter(parish_id=parish_id).values('id', 'name')
    print(f"Filtered communities: {communities}")
    return JsonResponse({'communities': list(communities)})

def get_communities(request):
    parish_id = request.GET.get('parish', None)
    communities = CommunityCode.objects.filter(parish_id=parish_id).values('id', 'name')
    return JsonResponse(list(communities), safe=False)
# start address
def create_address(request, client_id):

    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #search_value = form.cleaned_data['community_search']
            #matching_addresses = Address.objects.filter(communitycode__name__icontains=search_value)

            address = form.save(commit=False)
            address.client = client
            address.facility_id = request.session['facility']
            address.created_by_id = request.session['User_id']
            address.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = AddressForm()
    return render(request, 'create_address.html', {'form': form, 'client': client})



def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    client = address.client
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.modified_by_id =  request.session['User_id']
            address.modified_on =  datetime.now()
            address.save()
            return render(request, 'close_window.html')
            #return redirect('address_list', {'address': address, 'address_id': address_id, 'client': client, 'client_id': client_id})
    else:
        form = AddressForm(instance=address)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_address.html', {'form': form, 'address': address})


def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    client = address.client
    if request.method == 'POST':
        address.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_address.html', {'address': address, 'client': client})


def address_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    addresses = Address.objects.filter(client_id=client_id)
    return render(request, 'address_list.html', {'addresses': addresses, 'client_id': client_id})

# end adddress

def create_arvmedication(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ARVMedicationForm(request.POST)
        if form.is_valid():
            arvmedication = form.save(commit=False)
            arvmedication.facility_id = request.session['facility']
            arvmedication.created_by_id = request.session['User_id']
            arvmedication.client = client
            arvmedication.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = ARVMedicationForm()
    return render(request, 'create_arvmedication.html', {'form': form, 'client': client})


def edit_arvmedication(request, arvmedication_id):
    arvmedication = get_object_or_404(ARVMedication, pk=arvmedication_id)
    client = arvmedication.client
    if request.method == 'POST':
        form = ARVMedicationForm(request.POST, instance=arvmedication)
        if form.is_valid():
            form.save()
            #return redirect('edit_client', client_id=client.id)
            return render(request, 'close_window.html')
    else:
        form = ARVMedicationForm(instance=arvmedication)
    return render(request, 'edit_arvmedication.html', {'form': form, 'arvmedication': arvmedication, 'arvmedication_id': arvmedication_id})


def delete_arvmedication(request, arvmedication_id):
    arvmedication = get_object_or_404(ARVMedication, pk=arvmedication_id)
    client = arvmedication.client
    if request.method == 'POST':
        arvmedication.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_arvmedication.html', {'arvmedication': arvmedication, 'client': client})


"""def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    address = Address.objects.filter(client_id=client_id)
    arvmedication = ARVMedication.objects.filter(client_id=client_id)
    #address = get_object_or_404(Address, client_id=client_id)
    #arvmedication = get_object_or_404(ARVMedication, client_id=client_id)
    return render(request, 'client_detail.html', {'client': client, 'address': address, 'arvmedication': arvmedication})
"""


def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    addresses = Address.objects.filter(client_id=client_id)
    arvmedication = ARVMedication.objects.filter(client_id=client_id)
    return render(request, 'client_detail.html', {'client': client, 'addresses': addresses, 'arvmedication': arvmedication})




def arvmedication_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    arvmedications = ARVMedication.objects.filter(client_id=client_id)
    return render(request, 'arvmedication_list.html', {'arvmedications': arvmedications, 'client_id': client_id})




def create_cd4count(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = CD4CountForm(request.POST)
        if form.is_valid():
            cd4 = form.save(commit=False)
            cd4.facility_id = request.session['facility']
            cd4.created_by_id = request.session['User_id']
            cd4.client = client
            cd4.save()
            return render(request, 'close_window.html')
    else:
        form = CD4CountForm()
    return render(request, 'create_cd4count.html', {'form': form, 'client': client})



def edit_cd4(request, cd4count_id):
    cd4count = get_object_or_404(CD4Count, pk=cd4count_id)
    client = cd4count.client
    if request.method == 'POST':
        form = CD4CountForm(request.POST, instance=cd4count)
        if form.is_valid():
            form.save()
            return render(request, 'close_window.html')
    else:
        form = CD4CountForm(instance=cd4count)
    return render(request, 'edit_cd4count.html', {'form': form, 'cd4count': cd4count, 'cd4count_id': cd4count_id})


def delete_cd4(request, cd4_id):
    cd4count = get_object_or_404(CD4Count, pk=cd4_id)
    client = cd4count.client
    if request.method == 'POST':
        cd4count.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_cd4.html', {'cd4count': cd4count, 'client': client})


def cd4_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    cd4s = CD4Count.objects.filter(client_id=client_id)
    return render(request, 'cd4_list.html', {'cd4s': cd4s, 'client_id': client_id})


# ---- viral load  ----
def create_viralload(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ViralLoadForm(request.POST)
        if form.is_valid():
            viralload = form.save(commit=False)
            viralload.facility_id = request.session['facility']
            viralload.created_by_id = request.session['User_id']
            viralload.client = client
            viralload.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = ViralLoadForm()
    return render(request, 'create_viralload.html', {'form': form, 'client': client})



def edit_viralload(request, viralload_id):
    viralload = get_object_or_404(ViralLoad, pk=viralload_id)
    client = viralload.client
    if request.method == 'POST':
        form = ViralLoadForm(request.POST, instance=viralload)
        if form.is_valid():
            form.save()
            return render(request, 'close_window.html')

            #return redirect('address_list', {'address': address, 'address_id': address_id, 'client': client, 'client_id': client_id})
    else:
        form = ViralLoadForm(instance=viralload)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_viralload.html', {'form': form, 'viralload': viralload})


def delete_viralload(request, viralload_id):
    viralload = get_object_or_404(ViralLoad, pk=viralload_id)
    client = viralload.client
    if request.method == 'POST':
        viralload.delete()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'delete_viralload.html', {'viralload': viralload, 'client': client})

def viralload_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    viralload = ViralLoad.objects.filter(client_id=client_id)
    return render(request, 'viralload_list.html', {'viralload': viralload, 'client_id': client_id})

# -- end viral load

# ---- Physical exam

def create_physicalexam(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = PhysicalExamForm(request.POST)
        if form.is_valid():
            physicalexam = form.save(commit=False)
            physicalexam.facility_id = request.session['facility']
            physicalexam.created_by_id = request.session['User_id']
            physicalexam.client = client
            physicalexam.save()
            return render(request, 'close_window.html')
            #return redirect('physicalexam_list', client_id=client_id)
    else:
        form = PhysicalExamForm()
    return render(request, 'create_physicalexam.html', {'form': form, 'client': client})



def edit_physicalexam(request, physicalexam_id):
    physicalexam = get_object_or_404(PhysicalExam, pk=physicalexam_id)
    client = physicalexam.client

    if request.method == 'POST':
        form = PhysicalExamForm(request.POST, instance=physicalexam)
        if form.is_valid():
            form.modified_by_id =  request.session['User_id']
            form.modified_on =  datetime.now()
            form.save()
            return render(request, 'close_window.html')
            #return redirect('physicalexam_list', client_id=client_id)
    else:
        form = PhysicalExamForm(instance=physicalexam)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_physicalexam.html', {'form': form, 'physicalexam': physicalexam})


def delete_physicalexam(request, physicalexam_id):
    physicalexam = get_object_or_404(PhysicalExam, pk=physicalexam_id)
    client = physicalexam.client
    if request.method == 'POST':
        physicalexam.delete()
        return redirect('client_list')
    return render(request, 'delete_physicalexam.html', {'physicalexam': physicalexam, 'client': client})


def physicalexam_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    physicalexam = PhysicalExam.objects.filter(client_id=client_id)
    return render(request, 'physicalexam_list.html', {'physicalexam': physicalexam, 'client_id': client_id})

# end Physical Exam




# ---- prep status  ----
def create_prepstatus(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = PrepStatusDetailForm(request.POST)
        if form.is_valid():
            prepstatus = form.save(commit=False)
            prepstatus.facility_id = request.session['facility']
            prepstatus.created_by_id = request.session['User_id']
            prepstatus.client = client
            prepstatus.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = PrepStatusDetailForm()
    return render(request, 'create_prepstatus.html', {'form': form, 'client': client})



def edit_prepstatus(request, prepstatus_id):
    prepstatus = get_object_or_404(PrepStatusDetail, pk=prepstatus_id)
    client = prepstatus.client
    if request.method == 'POST':
        form = PrepStatusDetailForm(request.POST, instance=prepstatus)
        if form.is_valid():
            form.save()
            return render(request, 'close_window.html')

            #return redirect('address_list', {'address': address, 'address_id': address_id, 'client': client, 'client_id': client_id})
    else:
        form = PrepStatusDetailForm(instance=prepstatus)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_prepstatus.html', {'form': form, 'prepstatus': prepstatus})


def delete_prepstatus(request, prepstatus_id):
    prepstatus = get_object_or_404(ViralLoad, pk=prepstatus_id)
    client = prepstatus.client
    if request.method == 'POST':
        prepstatus.delete()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'delete_prepstatus.html', {'prepstatus': prepstatus, 'client': client})

def prepstatus_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    prepstatus = PrepStatusDetail.objects.filter(client_id=client_id)
    return render(request, 'prepstatus_list.html', {'prepstatus': prepstatus, 'client_id': client_id})

# -- end viral load




# ---- social history  ----
def create_social(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = SocialForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.facility_id = request.session['facility']
            social.created_by_id = request.session['User_id']
            social.client = client
            social.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = SocialForm()
    return render(request, 'create_social.html', {'form': form, 'client': client})



def edit_social(request, social_id):
    social = get_object_or_404(SocialHistory, pk=social_id)
    client = social.client
    if request.method == 'POST':
        form = SocialForm(request.POST, instance=client)
        if form.is_valid():
            social1 = form.save(commit=False)
            social1.save()
            return render(request, 'close_window.html')
    else:
        form = SocialForm(instance=social)
    return render(request, 'edit_social.html', {'form': form, 'social': social})


def delete_social(request, social_id):
    social = get_object_or_404(SocialHistory, pk=social_id)
    client = social.client
    if request.method == 'POST':
        social.delete()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'delete_social.html', {'social': social, 'client': client})

def social_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    social = SocialHistory.objects.filter(client_id=client_id)
    return render(request, 'social_list.html', {'social': social, 'client_id': client_id})

# -- end social



# ---- social STI  ----
def create_sti(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = STI_TestsDoneForm(request.POST)
        if form.is_valid():
            sti = form.save(commit=False)
            sti.facility_id = request.session['facility']
            sti.created_by_id = request.session['User_id']
            sti.client = client
            sti.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = STI_TestsDoneForm()
    return render(request, 'create_sti.html', {'form': form, 'client': client})



def edit_sti(request, sti_id):
    sti = get_object_or_404(STI_TestsDone, pk=sti_id)
    client = sti.client
    if request.method == 'POST':
        form = STI_TestsDoneForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return render(request, 'close_window.html')
    else:
        form = STI_TestsDoneForm(instance=sti)
    return render(request, 'edit_sti.html', {'form': form, 'sti': sti})


def delete_sti(request, sti_id):
    sti = get_object_or_404(STI_TestsDone, pk=sti_id)
    client = sti.client
    if request.method == 'POST':
        sti.delete()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'delete_sti.html', {'sti': sti, 'client': client})

def sti_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    sti = STI_TestsDone.objects.filter(client_id=client_id)
    return render(request, 'sti_list.html', {'sti': sti, 'client_id': client_id})

# -- end STI




# ----  Risk history ----
def create_risk(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.facility_id = request.session['facility']
            risk.created_by_id = request.session['User_id']
            risk.client = client
            risk.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = RiskForm()
    return render(request, 'create_risk.html', {'form': form, 'client': client})



def edit_risk(request, risk_id):
    risk = get_object_or_404(RiskHistory, pk=risk_id)
    client = risk.client
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return render(request, 'close_window.html')
    else:
        form = RiskForm(instance=risk)
    return render(request, 'edit_risk.html', {'form': form, 'risk': risk})


def delete_risk(request, risk_id):
    risk = get_object_or_404(RiskHistory, pk=risk_id)
    client = risk.client
    if request.method == 'POST':
        risk.delete()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'delete_risk.html', {'risk': risk, 'client': client})

def risk_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    risk = RiskHistory.objects.filter(client_id=client_id)
    return render(request, 'risk_list.html', {'risk': risk, 'client_id': client_id})

# -- end Risk


# ------ risk assessment

def create_riskassessment(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            riskassessment = form.save(commit=False)
            riskassessment.client = client
            riskassessment.facility_id = request.session['facility']
            riskassessment.created_by_id = request.session['User_id']
            riskassessment.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = RiskAssessmentForm()
    return render(request, 'create_riskassessment.html', {'form': form, 'client': client})



def edit_riskassessment(request, riskassessment_id):
    riskassessment = get_object_or_404(RiskAssessment, pk=riskassessment_id)
    client = riskassessment.client
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST, instance=riskassessment)
        if form.is_valid():
            riskassessment = form.save(commit=False)
            riskassessment.modified_by_id =  request.session['User_id']
            riskassessment.modified_on =  datetime.now()
            riskassessment.save()
            return render(request, 'close_window.html')
            #return redirect('address_list', {'address': address, 'address_id': address_id, 'client': client, 'client_id': client_id})
    else:
        form = RiskAssessmentForm(instance=riskassessment)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_riskassessment.html', {'form': form, 'riskassessment': riskassessment})


def delete_riskassessment(request, riskassessment_id):
    riskassessment = get_object_or_404(RiskAssessment, pk=riskassessment_id)
    client = riskassessment.client
    if request.method == 'POST':
        riskassessment.delete()
        return redirect('edit_riskassessment', client_id=client.id)
    return render(request, 'delete_riskassessment.html', {'riskassessment': riskassessment, 'client': client})


def riskassessment_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    riskassessment = RiskAssessment.objects.filter(client_id=client_id)
    return render(request, 'riskassessment_list.html', {'riskassessment': riskassessment, 'client_id': client_id})

# ------ risk assessment


#----- Prep eligibility

def create_prepeligibility(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = PrepEligibilityForm(request.POST)
        if form.is_valid():
            prepeligibility = form.save(commit=False)
            prepeligibility.client = client
            prepeligibility.facility_id = request.session['facility']
            prepeligibility.created_by_id = request.session['User_id']
            prepeligibility.save()
            return render(request, 'close_window.html')
    else:
        form = PrepEligibilityForm()
    return render(request, 'create_prepeligibility.html', {'form': form, 'client': client})



def edit_prepeligibility(request, prepeligibility_id):
    prepeligibility = get_object_or_404(PrepEligibility, pk=prepeligibility_id)
    client = prepeligibility.client
    if request.method == 'POST':
        form = PrepEligibilityForm(request.POST, instance=prepeligibility)
        if form.is_valid():
            prepeligibility = form.save(commit=False)
            prepeligibility.modified_by_id =  request.session['User_id']
            prepeligibility.modified_on =  datetime.now()
            prepeligibility.save()
            return render(request, 'close_window.html')
    else:
        form = PrepEligibilityForm(instance=prepeligibility)
    return render(request, 'edit_prepeligibility.html', {'form': form, 'prepeligibility': prepeligibility})


def delete_prepeligibility(request, prepeligibility_id):
    prepeligibility = get_object_or_404(PrepEligibility, pk=prepeligibility_id)
    client = prepeligibility.client
    if request.method == 'POST':
        prepeligibility.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_prepeligibility.html', {'prepeligibility': prepeligibility, 'client': client})


def prepeligibility_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    prepeligibility = PrepEligibility.objects.filter(client_id=client_id)
    return render(request, 'prepeligibility_list.html', {'prepeligibility': prepeligibility, 'client_id': client_id})





def create_sexualhistory(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = SexualHistoryForm(request.POST)
        if form.is_valid():
            sexualhistory = form.save(commit=False)
            sexualhistory.client = client
            sexualhistory.facility_id = request.session['facility']
            sexualhistory.created_by_id = request.session['User_id']
            sexualhistory.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = SexualHistoryForm()
    return render(request, 'create_sexualhistory.html', {'form': form, 'client': client})



def edit_sexualhistory(request, sexualhistory_id):
    sexualhistory = get_object_or_404(SexualHistory, pk=sexualhistory_id)
    client = sexualhistory.client
    if request.method == 'POST':
        form = SexualHistoryForm(request.POST, instance=sexualhistory)
        if form.is_valid():
            sexualhistory = form.save(commit=False)
            sexualhistory.modified_by_id =  request.session['User_id']
            sexualhistory.modified_on =  datetime.now()
            sexualhistory.save()
            return render(request, 'close_window.html')
    else:
        form = SexualHistoryForm(instance=sexualhistory)
    return render(request, 'edit_sexualhistory.html', {'form': form, 'sexualhistory': sexualhistory})


def delete_sexualhistory(request, sexualhistory_id):
    sexualhistory = get_object_or_404(SexualHistory, pk=sexualhistory_id)
    client = sexualhistory.client
    if request.method == 'POST':
        sexualhistory.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_sexualhistory.html', {'sexualhistory': sexualhistory, 'client': client})


def sexualhistory_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    sexualhistory = SexualHistory.objects.filter(client_id=client_id)
    return render(request, 'sexualhistory_list.html', {'sexualhistory': sexualhistory, 'client_id': client_id})


#New docket model
def create_docketnew(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = DocketNewForm(request.POST)
        if form.is_valid():
            docketnew = form.save(commit=False)
            docketnew.facility_id = request.session['facility']
            docketnew.created_by_id = request.session['User_id']
            docketnew.client = client
            docketnew.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = DocketNewForm()
    return render(request, 'create_docketnew.html', {'form': form, 'client': client})



def docketnew_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    docket = Docket_new.objects.filter(client_id=client_id)
    return render(request, 'docket_list.html', {'docket': docket, 'client_id': client_id})



def edit_docketnew(request, docket_id):
    docket = get_object_or_404(Docket_new, pk=docket_id)
    client = docket.client

    if request.method == 'POST':
        form = DocketNewForm(request.POST, instance=docket)
        if form.is_valid():
            form.modified_by_id =  request.session['User_id']
            form.facility_id = request.session['facility']
            form.modified_on =  datetime.now()
            form.save()
            return render(request, 'close_window.html')
            #return redirect('physicalexam_list', client_id=client_id)
    else:
        form = DocketNewForm(instance=docket)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_docket.html', {'form': form, 'docket': docket})


def delete_docketnew(request, docket_id):
    docket = get_object_or_404(Docket_new, pk=docket_id)
    client = docket.client
    if request.method == 'POST':
        docket.delete()
        return redirect('client_list')
    return render(request, 'delete_docket.html', {'docket': docket, 'client': client})
# end Dockets



#Out of care status model
def create_outofcarestatus(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = OutOfCareStatusForm(request.POST)
        if form.is_valid():
            oocs = form.save(commit=False)
            oocs.facility_id = request.session['facility']
            oocs.created_by_id = request.session['User_id']
            oocs.client = client
            oocs.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = OutOfCareStatusForm()
    return render(request, 'create_outofcarestatus.html', {'form': form, 'client': client})



def outofcarestatus_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    oocs = OutOfCareStatus.objects.filter(client_id=client_id)
    return render(request, 'outofcarestatus_list.html', {'oocs': oocs, 'client_id': client_id})



def edit_outofcarestatus(request, outofcarestatus_id):
    outofcarestatus = get_object_or_404(OutOfCareStatus, pk=outofcarestatus_id)
    client = outofcarestatus.client

    if request.method == 'POST':
        form = OutOfCareStatusForm(request.POST, instance=outofcarestatus)
        if form.is_valid():
            form.modified_by_id =  request.session['User_id']
            form.facility_id = request.session['facility']

            form.modified_on =  datetime.now()
            form.save()
            return render(request, 'close_window.html')
    else:
        form = OutOfCareStatusForm(instance=outofcarestatus)
    return render(request, 'edit_outofcarestatus.html', {'form': form, 'outofcarestatus': outofcarestatus})


def delete_outofcarestatus(request, outofcarestatus_id):
    outofcarestatus = get_object_or_404(OutOfCareStatus, pk=outofcarestatus_id)
    client = outofcarestatus.client
    if request.method == 'POST':
        outofcarestatus.delete()
        return redirect('client_list')
    return render(request, 'delete_outofcarestatus.html', {'outofcarestatus': outofcarestatus, 'client': client})
# end out of care status



#Liver Function
def create_liverkidney(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Liver_Kidney_TestsForm(request.POST)
        if form.is_valid():
            lf = form.save(commit=False)
            lf.facility_id = request.session['facility']
            lf.created_by_id = request.session['User_id']
            lf.client = client
            lf.save()
            return render(request, 'close_window.html')
            #return redirect('edit_client', client_id=client_id)
    else:
        form = Liver_Kidney_TestsForm()
    return render(request, 'create_liverkidney.html', {'form': form, 'client': client})



def liverkidney_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    liverkidney = Liver_Kidney_Tests.objects.filter(client_id=client_id)
    return render(request, 'liverkidney_list.html', {'liverkidney': liverkidney, 'client_id': client_id})



def edit_liverkidney(request, liverkidney_id):
    liverkidneytest = get_object_or_404(Liver_Kidney_Tests, pk=liverkidney_id)
    client = liverkidneytest.client

    if request.method == 'POST':
        form = Liver_Kidney_TestsForm(request.POST, instance=liverkidneytest)
        if form.is_valid():
            form.modified_by_id =  request.session['User_id']
            form.facility_id = request.session['facility']

            form.modified_on =  datetime.now()
            form.save()
            return render(request, 'close_window.html')
    else:
        form = Liver_Kidney_TestsForm(instance=liverkidneytest)
    return render(request, 'edit_liverkidney.html', {'form': form, 'liverkidneytest': liverkidneytest})


def delete_liverkidney(request, liverkidney_id):
    liverkidneytest = get_object_or_404(Liver_Kidney_Tests, pk=liverkidney_id)
    client = liverkidneytest.client
    if request.method == 'POST':
        liverkidneytest.delete()
        return redirect('client_list')
    return render(request, 'delete_liverkidney.html', {'liverkidneytest': liverkidneytest, 'client': client})
# end liver function



#start emergency contact

def create_emergencycontact(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergencycontact = form.save(commit=False)
            emergencycontact.client = client
            emergencycontact.facility_id = request.session['facility']
            emergencycontact.created_by_id = request.session['User_id']
            emergencycontact.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = EmergencyContactForm()
    return render(request, 'create_emergencycontact.html', {'form': form, 'client': client})



def edit_emergencycontact(request, emergencycontact_id):
    emergencycontact = get_object_or_404(EmergencyContact, pk=emergencycontact_id)
    client = emergencycontact.client
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=emergencycontact)
        if form.is_valid():
            emergencycontact = form.save(commit=False)
            emergencycontact.modified_by_id =  request.session['User_id']
            emergencycontact.modified_on =  datetime.now()
            emergencycontact.save()
            return render(request, 'close_window.html')
    else:
        form = EmergencyContactForm(instance=emergencycontact)
    return render(request, 'edit_emergencycontact.html', {'form': form, 'emergencycontact': emergencycontact})


def delete_emergencycontact(request, emergencycontact_id):
    emergencycontact = get_object_or_404(EmergencyContact, pk=emergencycontact_id)
    client = emergencycontact.client
    if request.method == 'POST':
        emergencycontact.delete()
        return redirect('edit_emergencycontact', client_id=client.id)
    return render(request, 'delete_emergencycontact.html', {'emergencycontact': emergencycontact, 'client': client})


def emergencycontact_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    emergencycontact = EmergencyContact.objects.filter(client_id=client_id)
    return render(request, 'emergencycontact_list.html', {'emergencycontact': emergencycontact, 'client_id': client_id})


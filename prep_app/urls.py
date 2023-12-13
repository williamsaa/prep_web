# client/urls.py

from django.urls import path
from .views import (
    close_window, fetch_communities, get_communities,
    client_list,  create_client,  edit_client,  delete_client,  client_detail,
    create_address, edit_address,  delete_address,  address_list,
    create_arvmedication,   edit_arvmedication,     delete_arvmedication, arvmedication_list,
    cd4_list,     edit_cd4,     create_cd4count,     delete_cd4,
    viralload_list,     edit_viralload,     create_viralload,     delete_viralload,
    physicalexam_list,     edit_physicalexam,     create_physicalexam,     delete_physicalexam,
    docketnew_list, edit_docketnew, create_docketnew, delete_docketnew,
    prepstatus_list, edit_prepstatus, create_prepstatus, delete_prepstatus,
    social_list, edit_social, create_social, delete_social,

    sti_list, edit_sti, create_sti, delete_sti,
    risk_list, create_risk, edit_risk, delete_risk,
    riskassessment_list, edit_riskassessment, create_riskassessment, delete_riskassessment,
    prepeligibility_list, edit_prepeligibility, create_prepeligibility, delete_prepeligibility,

    sexualhistory_list, edit_sexualhistory, create_sexualhistory, delete_sexualhistory,

    edit_outofcarestatus, create_outofcarestatus, delete_outofcarestatus, outofcarestatus_list,
    liverkidney_list, edit_liverkidney, create_liverkidney, delete_liverkidney,
    emergencycontact_list, edit_emergencycontact, create_emergencycontact, delete_emergencycontact,

    reports1, 

)

urlpatterns = [
    path('get_communities/', get_communities, name='get_communities'),
    path('reports1/', reports1, name='reports1'),
    path('close_window/', close_window, name='close_window'),
    path('list/', client_list, name='client_list'),
    path('create/', create_client, name='create_client'),
    path('edit/<int:client_id>/', edit_client, name='edit_client'),
    path('delete/<int:client_id>/', delete_client, name='delete_client'),
    path('create/address/<int:client_id>/', create_address, name='create_address'),
    path('edit/address/<int:address_id>/', edit_address, name='edit_address'),
    path('delete/address/<int:address_id>/', delete_address, name='delete_address'),
    path('create/arvmedication/<int:client_id>/', create_arvmedication, name='create_arvmedication'),
    path('edit/arvmedication/<int:arvmedication_id>/', edit_arvmedication, name='edit_arvmedication'),
    path('delete/arvmedication/<int:arvmedication_id>/', delete_arvmedication, name='delete_arvmedication'),
    path('arvmedication_list/<int:client_id>/', arvmedication_list, name='arvmedication_list'),

    path('create/cd4/<int:client_id>/', create_cd4count, name='create_cd4count'),
    path('edit/cd4/<int:cd4count_id>/', edit_cd4, name='edit_cd4'),
    path('delete/cd4/<int:cd4_id>/', delete_cd4, name='delete_cd4'),
    path('cd4_list/<int:client_id>/', cd4_list, name='cd4_list'),

    path('create/viralload/<int:client_id>/', create_viralload, name='create_viralload'),
    path('edit/viralload/<int:viralload_id>/', edit_viralload, name='edit_viralload'),
    path('delete/viralload/<int:viralload_id>/', delete_viralload, name='delete_viralload'),
    path('viralload_list/<int:client_id>/', viralload_list, name='viralload_list'),

    path('create/physicalexam/<int:client_id>/', create_physicalexam, name='create_physicalexam'),
    path('edit/physicalexam/<int:physicalexam_id>/', edit_physicalexam, name='edit_physicalexam'),
    path('delete/physicalexam/<int:physicalexam_id>/', delete_physicalexam, name='delete_physicalexam'),
    path('physicalexam_list/<int:client_id>/', physicalexam_list, name='physicalexam_list'),

    path('detail/<int:client_id>/', client_detail, name='client_detail'),
    #path('address_list/', address_list, name='address_list'),
    #path('client/edit/address/<int:address_id>/<int:client_id>/', edit_address, name='edit_address'),
    path('address_list/<int:client_id>/', address_list, name='address_list'),
    #path('client/address_list/<int:client_id>/', address_list, name='address_list'),
    path('create/address/<int:client_id>/', create_address, name='create_address'),
    

    path('create/docket/<int:client_id>/', create_docketnew, name='create_docket'),
    path('edit/docket/<int:docket_id>/', edit_docketnew, name='edit_docket'),
    path('delete/docket/<int:docket_id>/', delete_docketnew, name='delete_docket'),



    path('create/prepstatus/<int:client_id>/', create_prepstatus, name='create_prepstatus'),
    path('edit/prepstatus/<int:prepstatus_id>/', edit_prepstatus, name='edit_prepstatus'),
    path('delete/prepstatus/<int:prepstatus_id>/', delete_prepstatus, name='delete_prepstatus'),
    path('prepstatus_list/<int:client_id>/', prepstatus_list, name='prepstatus_list'),

    path('create/social/<int:client_id>/', create_social, name='create_social'),
    path('edit/social/<int:social_id>/', edit_social, name='edit_social'),
    path('delete/social/<int:social_id>/', delete_social, name='delete_social'),
    path('social_list/<int:client_id>/', social_list, name='social_list'),

    path('create/sti/<int:client_id>/', create_sti, name='create_sti'),
    path('edit/sti/<int:sti_id>/', edit_sti, name='edit_sti'),
    path('delete/sti/<int:sti_id>/', delete_sti, name='delete_sti'),
    path('sti_list/<int:client_id>/', sti_list, name='sti_list'),


    path('create/risk/<int:client_id>/', create_risk, name='create_risk'),
    path('edit/risk/<int:risk_id>/', edit_risk, name='edit_risk'),
    path('delete/risk/<int:risk_id>/', delete_risk, name='delete_risk'),
    path('risk_list/<int:client_id>/', risk_list, name='risk_list'),


    path('create/riskassessment/<int:client_id>/', create_riskassessment, name='create_riskassessment'),
    path('edit/riskassessment/<int:riskassessment_id>/', edit_riskassessment, name='edit_riskassessment'),
    path('delete/riskassessment/<int:riskassessment_id>/', delete_riskassessment, name='delete_riskassessment'),
    path('riskassessment_list/<int:client_id>/', riskassessment_list, name='riskassessment_list'),


    path('create/prepeligibility/<int:client_id>/', create_prepeligibility, name='create_prepeligibility'),
    path('edit/prepeligibility/<int:prepeligibility_id>/', edit_prepeligibility, name='edit_prepeligibility'),
    path('delete/prepeligibility/<int:prepeligibility_id>/', delete_prepeligibility, name='delete_prepeligibility'),
    path('prepeligibility_list/<int:client_id>/', prepeligibility_list, name='prepeligibility_list'),

    path('create/sexualhistory/<int:client_id>/', create_sexualhistory, name='create_sexualhistory'),
    path('edit/sexualhistory/<int:sexualhistory_id>/', edit_sexualhistory, name='edit_sexualhistory'),
    path('delete/sexualhistory/<int:sexualhistory_id>/', delete_sexualhistory, name='delete_sexualhistory'),
    path('sexualhistory_list/<int:client_id>/', sexualhistory_list, name='sexualhistory_list'),

    path('create/docketnew/<int:client_id>/', create_docketnew, name='create_docketnew'),
    path('docketnew_list/<int:client_id>/', docketnew_list, name='docketnew_list'),

    path('create/outofcarestatus/<int:client_id>/', create_outofcarestatus, name='create_outofcarestatus'),
    path('edit/outofcarestatus/<int:outofcarestatus_id>/', edit_outofcarestatus, name='edit_outofcarestatus'),
    path('delete/outofcarestatus/<int:outofcarestatus_id>/', delete_outofcarestatus, name='delete_outofcarestatus'),
    path('outofcarestatus_list/<int:client_id>/', outofcarestatus_list, name='outofcarestatus_list'),

    path('create/liverkidney/<int:client_id>/', create_liverkidney, name='create_liverkidney'),
    path('edit/liverkidney/<int:liverkidney_id>/', edit_liverkidney, name='edit_liverkidney'),
    path('delete/liverkidney/<int:liverkidney_id>/', delete_liverkidney, name='delete_liverkidney'),
    path('liverkidney_list/<int:client_id>/', liverkidney_list, name='liverkidney_list'),

    path('create/emergencycontact/<int:client_id>/', create_emergencycontact, name='create_emergencycontact'),
    path('edit/emergencycontact/<int:emergencycontact_id>/', edit_emergencycontact, name='edit_emergencycontact'),
    path('delete/emergencycontact/<int:emergencycontacty_id>/', delete_emergencycontact, name='delete_emergencycontact'),
    path('emergencycontact_list/<int:client_id>/', emergencycontact_list, name='emergencycontact_list'),


    path('fetch_communities/', fetch_communities, name='fetch_communities'), 




]

# client/forms.py

from django import forms
from dal import autocomplete, forward

from .models import Client,  ARVMedication, Address, CD4Count, ViralLoad, PhysicalExam, PrepStatusDetail, SocialHistory, RiskHistory, EmergencyContact, STI_TestsDone, RiskAssessment, PrepEligibility, SexualHistory, Docket_new, OutOfCareStatus, Liver_Kidney_Tests, UserFacilityAssignment, EmergencyContact
from .models import YesNoCode, CommunityCode
#from crispy_forms.layout import Layout, Fieldset
from crispy_forms.helper import FormHelper

from django.utils.encoding import force_str

from django_flatpickr.widgets import DatePickerInput
from crispy_forms.layout import Layout, Fieldset, Div, HTML
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from dateutil.relativedelta import *


UserFacilityAssignmentFormSet = inlineformset_factory(User, UserFacilityAssignment, fields=('facility', 'date'), fk_name='user')


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be greater than today.")


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
        }
    #date = forms.DateField(validators=[validate_not_future_date])


class PrepEligibilityForm(forms.ModelForm):
    class Meta:
        model = PrepEligibility
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "assessment_date": DatePickerInput(),
        }
    #assessment_date = forms.DateField(validators=[validate_not_future_date])


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            "date_of_birth": DatePickerInput(),
         }
    #date_of_birth = forms.DateField(validators=[validate_not_future_date])



class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = 'date_at_address', 'street_name', 'parish', 'community', 'telephone_cell1', 'telephone_cell2', 'notes'
        #widgets = {
        #    'parish': forms.Select(attrs={'class': 'form-select', 'id': 'id_parish'}),
        #    'community': forms.Select(attrs={'class': 'form-select', 'id': 'id_community'}),
        # }
        
        widgets = {
            "date_at_address": DatePickerInput(),
        }

        #class Media:
        #        js = ('js/community_dropdown.js',)
    #date_at_address = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}))
    #date_at_address = forms.DateField(validators=[validate_not_future_date])








class ARVMedicationForm(forms.ModelForm):
    class Meta:
        model = ARVMedication
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "report_date": DatePickerInput(),
            "due_date": DatePickerInput(),
         }
    #report_date = forms.DateField(validators=[validate_not_future_date])


class CD4CountForm(forms.ModelForm):
    class Meta:
        model = CD4Count
        fields = 'test_date', 'test_result', 'notes'
        widgets = {
            "test_date": DatePickerInput(),
         }
    #test_date = forms.DateField(validators=[validate_not_future_date])


class ViralLoadForm(forms.ModelForm):
    class Meta:
        model = ViralLoad
        fields = 'test_date', 'is_viral_load_request','test_result',  'undetectable','notes'
        widgets = {
            "test_date": DatePickerInput(),
         }
    #test_date = forms.DateField(validators=[validate_not_future_date])


class PhysicalExamForm(forms.ModelForm):
    class Meta:
        model = PhysicalExam
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']




class PrepStatusDetailForm(forms.ModelForm):
    class Meta:
        model = PrepStatusDetail
        fields = 'status_date', 'prepstatus'
        widgets = {
            "status_date": DatePickerInput(),
         }
    #status_date = forms.DateField(validators=[validate_not_future_date])


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialHistory
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
         }
    #date = forms.DateField(validators=[validate_not_future_date])




class RiskForm(forms.ModelForm):
    class Meta:
        model = RiskHistory
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by','client', 'facility']
        widgets = {
            "date": DatePickerInput(),
         }
    #date = forms.DateField(validators=[validate_not_future_date])



class STI_TestsDoneForm(forms.ModelForm):
    class Meta:
        model = STI_TestsDone
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility', 'deactivated_at']

        widgets = {
            "test_date": DatePickerInput(),
         }
    #test_date = forms.DateField(validators=[validate_not_future_date])



class SexualHistoryForm(forms.ModelForm):
    class Meta:
        model = SexualHistory
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility', 'deactivated_at']

        widgets = {
            "interview_date": DatePickerInput(),
            "last_sexual_encounter": DatePickerInput(),
            "lmp_date": DatePickerInput(),
         }
    #interview_date = forms.DateField(validators=[validate_not_future_date])
    #last_sexual_encounter = forms.DateField(validators=[validate_not_future_date])
    #lmp_date = forms.DateField(validators=[validate_not_future_date])



class RiskAssessmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

    class Meta:
        model = RiskAssessment
        fields = [
        'performed_by', 
        'risk_keypop_profile',
        'sex_partner_hiv_positive',
        'sex_partner_hiv_positive_not_on_art',
        'sex_partner_hiv_positive_on_art_6months',
        'sex_partner_hiv_positive_suspected_poor_adherence_to_art',
        'sex_partner_hiv_positive_detectable_hiv_viral_load',
        'sex_partner_hiv_positive_couple_trying_to_conceive',
        'sex_partner_high_risk_and_hiv_status_unknown',
        'has_sex_with_multiple_partners',
        'ongoing_ipv_gbv',
        'transactional_sex',
        'recent_sti_6months',
        'recurrent_use_pep',
        'recurrent_sex_under_influence_of_alcohol_drugs',
        'inconsistent_or_no_condom_use',
        'shared_needles_or_syringes',
        'blood_pressure',
        'weight_kg',
        'height_cm',
        'signs_of_sti',
        'liver_disease_treatment',
        'kidney_disease_treatment',
        'chronic_illness_other',
        'male_circumcised',
        'lmp_date',
        'pregnant',
        'if_pregnant',
        'breast_feeding',
        'family_planning_female',
        'plan_to_have_children',
        'clinical_notes',
        'hepatitis_b_results',
        'hepatitis_c_results',
        'serum_creatinine',
        'serum_creatinine_result',
        'prep_initiation_additional_steps',
        'previous_prep_use',
        'condoms_issued',
        'willing_to_start_prep',
        'adherence_counseling_done',
        'reason_not_will_to_start_prep',
        'signs_of_acute_hiv',
        'medically_ineligible_to_start_prep',
        'contraindications_for_TDF_FTC_TDF_3TC_TDF',
        'prescribed_prep_at_initial_visit',
        'prescribed_prep_at_initial_visit_regime',
        'prescribed_prep_at_initial_visit_regime_months_duration',
        'prescribed_prep_at_initial_visit_date_of_initiation']

        widgets = {
            "interview_date": DatePickerInput(),
            "last_sexual_encounter": DatePickerInput(),
            "lmp_date": DatePickerInput(),
         }


class DocketNewForm(forms.ModelForm):
    class Meta:
        model = Docket_new
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility', 'deactivated_at']

        #widgets = {
        #    "date_created": DatePickerInput(),
        # }

        widgets = {
            "date_created": DatePickerInput(attrs={'max': timezone.now().strftime('%Y-%m-%d')}),
        }

        
    #date_created = forms.DateField(validators=[validate_not_future_date])


class OutOfCareStatusForm(forms.ModelForm):
    class Meta:
        model = OutOfCareStatus
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility', 'deactivated_at']

        widgets = {
            "status_date": DatePickerInput(),
         }
    #status_date = forms.DateField(validators=[validate_not_future_date])


class Liver_Kidney_TestsForm(forms.ModelForm):
    class Meta:
        model = Liver_Kidney_Tests
        #fields = 'status_date', 'prepstatus'
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility', 'deactivated_at']

        widgets = {
            "test_date": DatePickerInput(),
         }
    #test_date = forms.DateField(validators=[validate_not_future_date])


# client/models.py
from datetime import datetime
import django
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .base_model import TSIS2BaseModel
from django.db.models import CheckConstraint, Q
from django.core.exceptions import ValidationError



import re
CONDOM_USE = (
    ('< 1/2 the time','< 1/2 the time'),
    ('> 1/2 the time','> 1/2 the time'),
    ('Never','Never'),
)

HIV_Result = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Unknown', 'Unknown'),
    )

CURRENTGENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Trans: M to F', 'Trans: M to F'),
    ('Trans: F to M', 'Trans: F to M'),
    )

Sex_Partner_Gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Both', 'Both'),
    ('Other', 'Other'),
    )

def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be greater than today.")

class Client(TSIS2BaseModel):
    last_name = models.CharField(max_length=255, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    pet_name = models.CharField(max_length=255, blank=True, null=True)
    sex_at_birth = models.ForeignKey('GenderCode', blank=False, null=False, on_delete=models.PROTECT, default=1)
    current_gender =  models.CharField(max_length=255, choices = CURRENTGENDER, null=True)
    unique_identfier_code = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False, validators=[validate_not_future_date])
    marital_status = models.ForeignKey('MaritalStatusCode', blank=False, null=False, on_delete=models.PROTECT, default=1)
    death_date = models.DateField(blank=True, null=True)
    mother_last_name = models.CharField(max_length=255, blank=True, null=True)
    mother_first_name = models.CharField(max_length=255, blank=True, null=True)
    father_last_name = models.CharField(max_length=255, blank=True, null=True)
    father_first_name = models.CharField(max_length=255, blank=True, null=True)
    nhf_card = models.CharField(verbose_name='NHF Card', max_length=255, blank=True, null=True)
    trn_number = models.CharField(verbose_name='TRN Number', max_length=255, blank=True, null=True)
    cause_of_death = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        # Calculate the UIC based on the provided components
        unique_identfier_code = (
            self.last_name[:3] +          
            self.sex_at_birth.name[0] +
            str(self.date_of_birth.year)[-2:] +
            str(self.date_of_birth.day).zfill(2)
        )
        self.unique_identfier_code = unique_identfier_code
        super().save(*args, **kwargs)
# End Client model

# --------------------------------------------
class Address(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date_at_address = models.DateField(blank=False, null=False)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey("Parish", blank=False, null=False, on_delete=models.PROTECT)
    community =  models.CharField(max_length=255, blank=True, null=True)
    
    telephone_cell1 = models.CharField(max_length=255, blank=True, null=True)
    telephone_cell2 = models.CharField(max_length=255, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)



    def __str__(self):
        return "%s %s %s %s" % (self.client, " - ",self.street_name, self.community)

# --------------------------------------------
class ARVMedication(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    regimen = models.ForeignKey("Regimen", blank=False, null=False, on_delete=models.PROTECT)
    duration = models.ForeignKey("MonthDurationCode", blank=False, null=False, on_delete=models.PROTECT)
    report_date = models.DateField(blank=False, null=False)
    due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

    def __str__(self):
        return "%s %s %s" % (self.client, " - ",self.regimen)

    
# --------------------------------------------
class MonthDurationCode(models.Model):
    arv_duration = models.CharField(max_length=20, blank=False, null=False)
 
    def __str__(self):
        return "%s" % (self.arv_duration)

# --------------------------------------------
class GenderCode(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------
class MaritalStatusCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------
class ParishManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)


class Parish(TSIS2BaseModel):
    region  = models.ForeignKey("RegionCode", blank=False, null=False, on_delete=models.PROTECT)
    #1region = models.ForeignKey("Region", blank=False, null=False, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    abbreviation = models.CharField(max_length=10, blank=False, null=False, default="Unk")

    objects = ParishManager()

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
# --------------------------------------------
class RegionManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)


class RegionCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )
 # --------------------------------------------   
class Regimen(TSIS2BaseModel):
    line = models.ForeignKey("RegimenLineCode", blank=False, null=False, related_name="regimen_line", on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=False, null=False)
   
    def __str__(self):
        return "%s" % (self.name,)

    def natural_key(self):
        return (self.name, self.line, )
    
 # --------------------------------------------   
class RegimenLineCode(TSIS2BaseModel):
    line = models.IntegerField()
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.line)

    def natural_key(self):
        return (self.name, self.line, )
    
# --------------------------------------------

class CommunityManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)

class CommunityCode(models.Model):
    code = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    parish = models.ForeignKey("Parish", blank=False, null=False, on_delete=models.PROTECT)
    deactivated_at = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s" % (self.name)
    

# --------------------------------------------
class CD4Count(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    test_date = models.DateField(blank=False, null=False)
    test_result = models.IntegerField(blank=False, null=False)
    disa_reference_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

#    objects = CD4CountManager()

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('test_date', 'client',),)

    def __str__(self):
        return "%s" % (self.client)

    def natural_key(self):
        return (self.test_date, self.client )

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_test_date(validation_errors)
        self.validate_field_test_result(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def clean(self):
        super().clean()
        validation_errors = {}

        self.validate_field_test_date(validation_errors)
        self.validate_field_test_result(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)


    def validate_field_test_date(self, validation_errors):
        if hasattr(self, "test_date"):
            if self.test_date is not None:
                if self.test_date > datetime.now().date():
                    validation_errors["test_date"] = "Test date can not be in the future"
            else:
                validation_errors["test_date"] = "Test date must have a value"


    def validate_field_test_result(self, validation_errors):
        if hasattr(self, "test_result"):
            if self.test_result is not None:
                if self.test_result < 0 or self.test_result > 5000:
                    validation_errors["test_result"] = "Test result must be between 0 and 5000"
            else:
                validation_errors["test_result"] = "Test result must have a value"
# --------------------------------------------

class ViralLoad(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    is_viral_load_request = models.BooleanField(verbose_name='Sampling for Viral Load', default=False)
    test_date = models.DateField(blank=False, null=False)
    test_result = models.FloatField(blank=True, null=True)
    undetectable = models.BooleanField(default=False)
    disa_reference_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

# -----------------------
class YesNoCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )
    

# -----------------------
class OtherLab(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    facility = models.ForeignKey("Facility", blank=False, null=False, on_delete=models.PROTECT)
    test_date = models.DateField(blank=False, null=False)
    lab_test_name = models.ForeignKey("LabTestCode", blank=False, null=False, related_name='otherlab_lab_test_name', on_delete=models.PROTECT)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)
    def __str__(self):
        return "%s" % (self.test_date, self.client )

    def natural_key(self):
        return (self.test_date, self.client )

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_test_date(validation_errors)
        self.validate_field_lab_test_name(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_test_date(self, validation_errors):
        if hasattr(self, "test_date"):
            if self.test_date is not None:
                if self.test_date > datetime.now().date():
                    validation_errors["test_date"] = "Test date can not be in the future"
            else:
                validation_errors["test_date"] = "Test date must have a value"

    def validate_field_lab_test_name(self, validation_errors):
        if hasattr(self, "lab_test_name"):
            if self.lab_test_name is None :
                validation_errors['lab_test_name'] = 'Lab test name cannot be left blank'

# ---------------------------------

class EmergencyContact(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    relationship_to_patient = models.ForeignKey('RelationshipCode', blank=False, null=False, related_name="address_occupation", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    age_in_years = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    community =  models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey('Parish', blank=False, null=False, related_name="emergency_contact_parish", on_delete=models.PROTECT)
    telephone_cell = models.CharField(max_length=255, blank=True, null=True)
    telephone_home = models.CharField(max_length=255, blank=True, null=True)
    telephone_work = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

    readonly_fields = ('client',)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __str__(self):
        return "%s" % (self.client)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_community(validation_errors)
        self.validate_field_date(validation_errors)
        self.validate_field_first_name(validation_errors)
        self.validate_field_last_name(validation_errors)
        self.validate_field_parish(validation_errors)
        self.validate_field_relationship_to_patient(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_community(self, validation_errors):
        if hasattr(self, "community"):
            if self.community is None:
                validation_errors["community"] = "Community must have a value"

    def validate_field_date(self, validation_errors):
        if hasattr(self, "date"):
            if self.date is not None:
                if self.date > datetime.now().date():
                    validation_errors["date"] = "Date can not be in the future"
            else:
                validation_errors["date"] = "Date must have a value"

    def validate_field_first_name(self, validation_errors):
        if hasattr(self, "first_name"):
            if self.first_name is not None:
                if len(self.first_name) < 1 or len(self.first_name) > 50:
                    validation_errors['first_name'] = 'First name must be between 1 and 50 characters'

    def validate_field_last_name(self, validation_errors):
        if hasattr(self, "last_name"):
            if self.last_name is None:
                validation_errors['last_name'] = 'Last name must have a value'
            else:
                if len(self.last_name) < 1 or len(self.last_name) > 50:
                    validation_errors['last_name'] = 'Last name must be between 1 and 50 characters'

    def validate_field_parish(self, validation_errors):
        if hasattr(self, "parish"):
            if self.parish is None:
                validation_errors["parish"] = "Parish must have a value"

    def validate_field_relationship_to_patient(self, validation_errors):
        if hasattr(self, "relationship_to_patient"):
            if self.relationship_to_patient is None:
                validation_errors["relationship_to_patient"] = "Relationship to patient must have a value"
# --------------------------------------------

class RelationshipCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------

class Facility(TSIS2BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    lab_ref_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='LAB reference code')
    address1 = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey("Parish", blank=False, null=False,
                               related_name='facility_parish', on_delete=models.PROTECT)
    organization = models.ForeignKey("Organization", blank=False, null=False, related_name="facility_organization", on_delete=models.PROTECT)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )


# --------------------------------------------
class LabTestCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------
 
class OrganizationManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)

class Organization(TSIS2BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    #grant_organisation_wide_client_authorization1 = models.BooleanField(default=False)

    objects = OrganizationManager()

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('name', 'code', 'deleted_at'),)
        ordering = ['name']

    def __str__(self):
        return "%s %s" % (self.code, self.name)

    def natural_key(self):
        return self.name, self.code,

 # --------------------------------------------
class HivCategoryCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)


    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class RespiratoryRateCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class PapSmearResultCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class MammogramResultCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class UrinalysisCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class TreponemalResultCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class NonTreponemalResultCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class FamilyPlanningMethodCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
 # -----------------------
class PatientStabilityStatusCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
       
# ------------------------------- physical exam
class PhysicalExam(TSIS2BaseModel):
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    clinic_date = models.DateField(blank=False, null=False, default=datetime.now)
    examined_by = models.CharField(max_length=255, blank=False, null=False)
    presenting_complaints = models.TextField(blank=True, null=True)
    history_of_complaints = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    respiratory_rate = models.ForeignKey('RespiratoryRateCode', blank=False, null=False, on_delete=models.PROTECT, default=0)
    blood_pressure = models.CharField(max_length=255, blank=True, null=True)
    hiv_category = models.ForeignKey('HivCategoryCode', blank=False, null=False, on_delete=models.PROTECT,default=0)
    bmi = models.FloatField(blank=True, null=True)
    smoker = models.ForeignKey("YesNoCode", blank=False, null=False, related_name="physical_exam_smoker", on_delete=models.PROTECT, default=0)
    pap_smear_done = models.ForeignKey("YesNoCode", blank=False, null=False, related_name="physical_exam_pap_smear_done", on_delete=models.PROTECT, default=0)
    pap_smear_date = models.DateField(blank=True, null=True)
    pap_smear_result = models.ForeignKey('PapSmearResultCode', blank=False, null=False, related_name="physical_exam_pap_smear_result", on_delete=models.PROTECT, default=0)
    mammogram_done = models.ForeignKey("YesNoCode", blank=False, null=False,
                                       related_name="physical_exam_mammogram_done", on_delete=models.PROTECT,default=0)
    mammogram_date = models.DateField(blank=True, null=True)
    mammogram_result = models.ForeignKey('MammogramResultCode', blank=False, null=False, on_delete=models.PROTECT, default=0)
    anal_pap_smear_date = models.DateField(blank=True, null=True)
    anal_pap_smear_done = models.ForeignKey("YesNoCode", blank=False, null=False,
                                            related_name="physical_exam_anal_pap_smear_done", on_delete=models.PROTECT, default=0)
    anal_pap_smear_result = models.ForeignKey('PapSmearResultCode', blank=False, null=False,
                                              related_name="physical_exam_anal_pap_smear_result",
                                              on_delete=models.PROTECT,default=0)
    psa_done = models.ForeignKey("YesNoCode", blank=False, null=False, related_name="physical_exam_psa_done", on_delete=models.PROTECT, default=0)
    psa_date = models.DateField(blank=True, null=True)
    psa_result = models.ForeignKey('PapSmearResultCode', blank=False, null=False, related_name="physical_exam_psa_result", on_delete=models.PROTECT,default=0)
    notes = models.TextField(blank=True, null=True)

    temperature = models.FloatField(blank=True, null=True)
    last_menstrual_period = models.DateField(blank=True, null=True)
    pregnant = models.ForeignKey("YesNoCode", blank=False, null=False, related_name="physical_exam_pregnant", on_delete=models.PROTECT, default=0)
    pregnant_edd = models.DateField(blank=True, null=True)
    next_appointment_date = models.DateField(blank=True, null=True)

    urinalysis = models.ForeignKey('UrinalysisCode', blank=False, null=False, related_name="physical_exam_urinalysis", on_delete=models.PROTECT, default=0)
    syphilis_treponemal_resultdate = models.DateField(blank=True, null=True)
    syphilis_non_treponemal_resultdate = models.DateField(blank=True, null=True)
    syphilis_done = models.ForeignKey("YesNoCode", blank=False, null=False, related_name="physical_exam_syphilis_done",
                                 on_delete=models.PROTECT, default=0)
    treponemal_result = models.ForeignKey('TreponemalResultCode', blank=False, null=False, related_name="physical_exam_treponemal_result", on_delete=models.PROTECT, default=0)
    nontreponemal_result = models.ForeignKey('NonTreponemalResultCode', blank=False, null=False, related_name="physical_exam_nontreponemal_result", on_delete=models.PROTECT, default=0)

    weight_loss = models.BooleanField(default=False)
    difficulty_breathing = models.BooleanField(default=False)
    cough = models.BooleanField(default=False)
    skin_rash = models.BooleanField(default=False)
    chect_pain = models.BooleanField(default=False)
    adbominal_pain = models.BooleanField(default=False)
    vomiting = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)
    dehydration = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    weakness = models.BooleanField(default=False)
    suicidal_thoughts = models.BooleanField(default=False)
    illegal_drugs = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    using_family_planning = models.BooleanField(default=False)
    family_planning_method = models.ForeignKey('FamilyPlanningMethodCode', blank=False, null=False, related_name="physical_exam_family_planning_method", on_delete=models.PROTECT)
    patient_stability_status = models.ForeignKey('PatientStabilityStatusCode', blank=False, null=False, related_name="physical_exam_patient_stability_status", on_delete=models.PROTECT)



    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __str__(self):
        return "%s" % (self.client)

    def natural_key(self):
        return (self.client)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_kept_appointment(validation_errors)
        self.validate_field_examined_by(validation_errors)
        self.validate_field_height(validation_errors)
        self.validate_field_hiv_category(validation_errors)
        self.validate_field_mammogram_date(validation_errors)
        self.validate_field_mammogram_done(validation_errors)
        self.validate_field_mammogram_result(validation_errors)
        self.validate_field_pap_smear_date(validation_errors)
        self.validate_field_pap_smear_done(validation_errors)
        self.validate_field_respiratory_rate(validation_errors)
        self.validate_field_smoker(validation_errors)
        self.validate_field_weight(validation_errors)

        self.validate_field_anal_pap_smear_done(validation_errors)
        self.validate_field_anal_pap_smear_date(validation_errors)
        self.validate_field_anal_pap_smear_result(validation_errors)
        self.validate_field_psa_done(validation_errors)
        self.validate_field_psa_date(validation_errors)
        self.validate_field_psa_result(validation_errors)
        self.validate_field_temperature(validation_errors)
        self.validate_field_last_menstrual_period(validation_errors)
        self.validate_field_pregnant(validation_errors)
        self.validate_field_pregnant_edd(validation_errors)
        self.validate_field_next_appointment_date(validation_errors)
        self.validate_field_urinalysis(validation_errors)
        self.validate_field_syphilis_treponemal_resultdate(validation_errors)
        self.validate_field_syphilis_non_treponemal_resultdate(validation_errors)
        self.validate_field_syphilis_done(validation_errors)
        self.validate_field_treponemal_result(validation_errors)
        self.validate_field_nontreponemal_result(validation_errors)
        self.validate_field_pap_smear_result(validation_errors)



        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_kept_appointment(self, validation_errors):
        if hasattr(self, "kept_appointment"):
            if self.kept_appointment is None:
                validation_errors["kept_appointment"] = "Kept appointment must have a value"

    def validate_field_examined_by(self, validation_errors):
        if hasattr(self, "examined_by"):
            if self.examined_by is None:
                validation_errors["examined_by"] = "examined_by must have a value"

    def validate_field_height(self, validation_errors):
        if hasattr(self, "height"):
            if self.height is not None:
                if self.height < 40 or self.height > 240:
                    validation_errors["height"] = "Height must be between 40 and 240"

    def validate_field_hiv_category(self, validation_errors):
        if hasattr(self, "hiv_category"):
            if self.hiv_category is None:
                validation_errors["hiv_category"] = "hiv_category must have a value"

    def validate_field_mammogram_date(self, validation_errors):
        if hasattr(self, "mammogram_date"):
            if self.mammogram_date is not None:
                if self.mammogram_date > datetime.now().date():
                    validation_errors["mammogram_date"] = "Mammogram date can not be in the future"
            # else:
            #     validation_errors["mammogram_date"] = "Mammogram date must have a value"

    def validate_field_mammogram_done(self, validation_errors):
        if hasattr(self, "mammogram_done"):
            if self.mammogram_done is None:
                validation_errors["mammogram_done"] = "mammogram_done must have a value"

    def validate_field_mammogram_result(self, validation_errors):
        if hasattr(self, "mammogram_result"):
            if self.mammogram_result is None:
                validation_errors["mammogram_result"] = "Mammogram result result must have a value"

    def validate_field_pap_smear_date(self, validation_errors):
        if hasattr(self, "pap_smear_date"):
            if self.pap_smear_date is not None:
                if self.pap_smear_date > datetime.now().date():
                    validation_errors["pap_smear_date"] = "Mammogram date can not be in the future"
            # else:
            #     validation_errors["pap_smear_date"] = "Pap_smear date must have a value"

    def validate_field_pap_smear_done(self, validation_errors):
        if hasattr(self, "pap_smear_done"):
            if self.pap_smear_done is None:
                validation_errors["pap_smear_done"] = "Pap smear done must have a value"

    def validate_field_respiratory_rate(self, validation_errors):
        if hasattr(self, "respiratory_rate"):
            if self.respiratory_rate is None:
                validation_errors["respiratory_rate"] = "Respiratory rate must have a value"

    def validate_field_smoker(self, validation_errors):
        if hasattr(self, "smoker"):
            if self.smoker is None:
                validation_errors["smoker"] = "Smoker must have a value"

    def validate_field_weight(self, validation_errors):
        if hasattr(self, "weight"):
            if self.weight is not None:
                if self.weight < 10 or self.weight > 300:
                    validation_errors["weight"] = "Weight must be between 10 and 300"


    def validate_field_anal_pap_smear_done(self, validation_errors):
        if hasattr(self, "anal_pap_smear_done"):
            if self.anal_pap_smear_done is None:
                validation_errors["anal_pap_smear_done"] = "anal_pap_smear_done must have a value"

    def validate_field_anal_pap_smear_date(self, validation_errors):
        if hasattr(self, "anal_pap_smear_date"):
            if self.anal_pap_smear_date is not None:
                if self.anal_pap_smear_date > datetime.now().date():
                    validation_errors["anal_pap_smear_date"] = "anal_pap_smear_date can not be in the future"


    def validate_field_anal_pap_smear_result(self, validation_errors):
        if hasattr(self, "anal_pap_smear_result"):
            if self.anal_pap_smear_result is None:
                validation_errors["anal_pap_smear_result"] = "anal_pap_smear_result result result must have a value"


    def validate_field_psa_done(self, validation_errors):
        if hasattr(self, "psa_done"):
            if self.psa_done is None:
                validation_errors["psa_done"] = "psa_done must have a value"


    def validate_field_psa_date(self, validation_errors):
        if hasattr(self, "psa_date"):
            if self.psa_date is not None:
                if self.psa_date > datetime.now().date():
                    validation_errors["psa_date"] = "psa_date can not be in the future"


    def validate_field_psa_result(self, validation_errors):
        if hasattr(self, "psa_result"):
            if self.psa_result is None:
                validation_errors["psa_result"] = "psa_result result result must have a value"


    def validate_field_temperature(self, validation_errors):
        if hasattr(self, "temperature"):
            if self.temperature is not None:
                if self.temperature < 20 or self.temperature > 50:
                    validation_errors["temperature"] = "temperature must be between 20 and 50"


    def validate_field_last_menstrual_period(self, validation_errors):
        if hasattr(self, "last_menstrual_period"):
            if self.last_menstrual_period is not None:
                if self.last_menstrual_period > datetime.now().date():
                    validation_errors["last_menstrual_period"] = "last_menstrual_period date can not be in the future"


    def validate_field_pregnant(self, validation_errors):
        if hasattr(self, "pregnant"):
            if self.pregnant is None:
                validation_errors["pregnant"] = "pregnant must have a value"


    def validate_field_pregnant_edd(self, validation_errors):
        if hasattr(self, "pregnant_edd"):
            if self.pregnant_edd is not None:
                if self.pregnant_edd > datetime.now().date():
                    validation_errors["pregnant_edd"] = "pregnant_edd date can not be in the future"


    def validate_field_next_appointment_date(self, validation_errors):
        if hasattr(self, "next_appointment_date"):
            if self.next_appointment_date is not None:
                if self.next_appointment_date < datetime.now().date():
                    validation_errors["next_appointment_date"] = "next_appointment date can not be in the past"


    def validate_field_urinalysis(self, validation_errors):
        if hasattr(self, "urinalysis"):
            if self.urinalysis is None:
                validation_errors["urinalysis"] = "urinalysis must have a value"



    def validate_field_syphilis_treponemal_resultdate(self, validation_errors):
        if hasattr(self, "syphilis_treponemal_resultdate"):
            if self.syphilis_treponemal_resultdate is not None:
                if self.syphilis_treponemal_resultdate > datetime.now().date():
                    validation_errors["syphilis_treponemal_resultdate"] = "syphilis_treponemal_result date can not be in the future"


    def validate_field_syphilis_non_treponemal_resultdate(self, validation_errors):
        if hasattr(self, "syphilis_non_treponemal_resultdate"):
            if self.syphilis_non_treponemal_resultdate is not None:
                if self.syphilis_non_treponemal_resultdate > datetime.now().date():
                    validation_errors["syphilis_non_treponemal_resultdate"] = "syphilis_non_treponemal_resultdate date can not be in the future"


    def validate_field_syphilis_done(self, validation_errors):
        if hasattr(self, "syphilis_done"):
            if self.syphilis_done is None:
                validation_errors["syphilis_done"] = "syphilis_done must have a value"



    def validate_field_treponemal_result(self, validation_errors):
        if hasattr(self, "treponemal_result"):
            if self.treponemal_result is None:
                validation_errors["treponemal_result"] = "treponemal_result must have a value"




    def validate_field_nontreponemal_result(self, validation_errors):
        if hasattr(self, "nontreponemal_result"):
            if self.nontreponemal_result is None:
                validation_errors["nontreponemal_result"] = "nontreponemal_result must have a value"




    def validate_field_pap_smear_result(self, validation_errors):
        if hasattr(self, "pap_smear_result"):
            if self.pap_smear_result is None:
                validation_errors["pap_smear_result"] = "pap_smear_result must have a value"

# ------------------------------- physical exam

class STI_Treatment(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)



class STI_TestCodes(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)

class STI_Results(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)
    
class STI_TestsDone(models.Model):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    test_date = models.DateField(blank=False, null=False)
    sti_test_name = models.ForeignKey("STI_TestCodes", blank=False, null=False, on_delete=models.PROTECT)
    test_results = models.ForeignKey("STI_Results", blank=False, null=False, on_delete=models.PROTECT)
    deactivated_at = models.BooleanField(default=False)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)
    #treatment_given = models.ForeignKey("STI_Treatment", blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "%s" % (self.name)


class PrepStatus(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)



class PrepStatusDetail(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    status_date = models.DateField(blank=False, null=False)
    prepstatus = models.ForeignKey("PrepStatus", blank=False, null=False, on_delete=models.PROTECT)
    deactivated_at = models.BooleanField(default=False)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.client, " - ",self.prepstatus)

    def validate_field_status_date(self, validation_errors):
        if hasattr(self, "status_date"):
            if self.status_date is not None:
                if self.status_date > datetime.now().date():
                    validation_errors["status_date"] = "Status date can not be in the future"
            else:
                validation_errors["status_date"] = "Status date must have a value"
#------------------------------------------------------


class UserFacilityAssignment(TSIS2BaseModel):

    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=True, null=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('user', 'facility'),)
        ordering = ['user__username', 'facility__name']

    def __str__(self):
        return "%s: %s-%s" % (self.date, self.user, self.facility)
    

#--------------------------------------------

# --------------- PastMedicalHistory
class PastMedicalHistory(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    performed_by = models.CharField(max_length=50, blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    past_medical_history = models.TextField(blank=True, null=True)
    major_surgery = models.TextField(blank=True, null=True)
    allergies_medication = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        ordering = ['-report_date']
        verbose_name_plural = "Past medical histories"

    def __str__(self):
        return "%s" % (self.report_date)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_report_date(validation_errors)
        self.validate_field_past_medical_historys(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_report_date(self, validation_errors):
        if hasattr(self, "report_date"):
            if self.report_date is not None:
                if self.report_date > datetime.now().date():
                    validation_errors["report_date"] = "Report date can not be in the future"
            else:
                validation_errors["report_date"] = "Report date must have a value"

    def validate_field_past_medical_historys(self, validation_errors):
        if hasattr(self, "past_medical_history"):
            if self.past_medical_history is None:
                validation_errors['past_medical_history'] = 'Past medical history cannot be left blank'
# --------------- PastMedicalHistory

class FrequencyCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)



class ContraceptiveMethodCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    

# --------------- RiskHistory
class RiskHistory(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    facility = models.ForeignKey("Facility", blank=False, null=False, on_delete=models.PROTECT)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    age_first_sex = models.IntegerField(blank=True, null=True)
    num_lifetime_partners = models.IntegerField(verbose_name='Number of Lifetime Partners', blank=True, null=True)
    condom_use = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='riskhistory_condom_use', on_delete=models.PROTECT)
    condom_use_other = models.CharField(max_length=255, blank=True, null=True)
    condom_use_during_last_sex = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_condom_use_during_last_sex', on_delete=models.PROTECT)
    condom_use_usual_partner = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='riskhistory_condom_use_usual_partner', on_delete=models.PROTECT)
    condom_use_usual_other = models.CharField(max_length=255, blank=True, null=True)
    condom_use_new_partner = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='riskhistory_condom_use_new_partner', on_delete=models.PROTECT)
    condom_use_new_other = models.CharField(max_length=255, blank=True, null=True)
    current_contraceptive_use = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_current_contraceptive_use', on_delete=models.PROTECT)
    current_contraceptive_method = models.ForeignKey("ContraceptiveMethodCode", blank=False, null=False, on_delete=models.PROTECT)
    current_contraceptive_method_other = models.CharField(max_length=255, blank=True, null=True)
    drug_use = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_drug_use', on_delete=models.PROTECT)
    tattoos = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_tattoos', on_delete=models.PROTECT)
    incarceration = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_incarceration', on_delete=models.PROTECT)
    csw = models.ForeignKey("YesNoCode", blank=False, null=False, verbose_name="CSW", related_name='riskhistory_csw', on_delete=models.PROTECT)
    sexual_abuse = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_sexual_abuse', on_delete=models.PROTECT)
    past_sti = models.ForeignKey("YesNoCode", blank=False, null=False, verbose_name="past STI", related_name='riskhistory_past_sti', on_delete=models.PROTECT)
    blood_transfusion = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_blood_transfusion', on_delete=models.PROTECT)
    transgender = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_transgender', on_delete=models.PROTECT)
    msm = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_msm', on_delete=models.PROTECT)
    pregnant = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='riskhistory_pregnant', on_delete=models.PROTECT)


    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        ordering = ['-date']
        verbose_name_plural = "Risk histories"

    def __str__(self):
        return "%s" % self.date

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_age_first_sex(validation_errors)
        self.validate_field_blood_transfusion(validation_errors)
        self.validate_field_condom_use_during_last_sex(validation_errors)
        self.validate_field_condom_use(validation_errors)
        self.validate_field_condom_use_new_partner(validation_errors)
        self.validate_field_condom_use_usual_partner(validation_errors)
        self.validate_field_csw(validation_errors)
        self.validate_field_current_contraceptive_method(validation_errors)
        self.validate_field_current_contraceptive_use(validation_errors)
        self.validate_field_date(validation_errors)
        self.validate_field_drug_use(validation_errors)
        self.validate_field_incarceration(validation_errors)
        self.validate_field_num_lifetime_partners(validation_errors)
        self.validate_field_past_sti(validation_errors)
        self.validate_field_pregnant(validation_errors)
        self.validate_field_sexual_abuse(validation_errors)
        self.validate_field_tattoos(validation_errors)
        self.validate_field_transgender(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)



    def clean(self):

        super().clean()

        validation_errors = {}

        self.validate_model_pregnant(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)


    def validate_model_pregnant(self, validation_errors):
        if self.pregnant_id is not None and self.client_id is not None:

            client = Client.objects.get(pk=self.client_id)

            if client.sex_at_birth.name == 'Male':
                yes = YesNoCode.objects.get(name="Yes")
                if self.pregnant_id == yes.id:
                    validation_errors["pregnant"] = "Males can not be pregnant"


    def validate_field_age_first_sex(self, validation_errors):
        if self.age_first_sex is not None:
            if self.age_first_sex < 5:
                validation_errors["age_first_sex"] = "Age must be greater than or equal to 5"
            if self.age_first_sex > 90:
                validation_errors["age_first_sex"] = "Age must be less that or equal to 90"

    def validate_field_blood_transfusion(self, validation_errors):
        if hasattr(self, "blood_transfusion"):
            if self.blood_transfusion is None:
                validation_errors["blood_transfusion"] = "Blood transfusion must have a selected value"

    def validate_field_condom_use_during_last_sex(self, validation_errors):
        if hasattr(self, "condom_use_during_last_sex"):
            if self.condom_use_during_last_sex is None:
                validation_errors["condom_use_during_last_sex"] = "Condom use during last sex must have a selected value"

    def validate_field_condom_use(self, validation_errors):
        if hasattr(self, "condom_use"):
            if self.condom_use is None:
                validation_errors["condom_use"] = "Condom use must have a selected value"

    def validate_field_condom_use_new_partner(self, validation_errors):
        if hasattr(self, "condom_use_new_partner"):
            if self.condom_use_new_partner is None:
                validation_errors["condom_use_new_partner"] = "Condom use with new partner must have a selected value"

    def validate_field_condom_use_usual_partner(self, validation_errors):
        if hasattr(self, "condom_use_usual_partner"):
            if self.condom_use_usual_partner is None:
                validation_errors["condom_use_usual_partner"] = "Condom use usual partner must have a selected value"

    def validate_field_csw(self, validation_errors):
        if hasattr(self, "csw"):
            if self.csw is None:
                validation_errors["csw"] = "CSW must have a selected value"

    def validate_field_current_contraceptive_method(self, validation_errors):
        if hasattr(self, "current_contraceptive_method"):
            if self.current_contraceptive_method is None:
                validation_errors["current_contraceptive_method"] = "Current contraceptive method must have a selected value"

    def validate_field_current_contraceptive_use(self, validation_errors):
        if hasattr(self, "current_contraceptive_use"):
            if self.current_contraceptive_use is None:
                validation_errors["current_contraceptive_use"] = "Current contraceptive use must have a selected value"

    def validate_field_date(self, validation_errors):
        if hasattr(self, "date"):
            if self.date is None:
                validation_errors["date"] = "Date must have a value"
            else:
                if self.date > timezone.now().date():
                    validation_errors["date"] = "Date can not be in the future"


    def validate_field_drug_use(self, validation_errors):
        if hasattr(self, "drug_use"):
            if self.drug_use is None:
                validation_errors["drug_use"] = "Drug use must have a selected value"

    def validate_field_incarceration(self, validation_errors):
        if hasattr(self, "incarceration"):
            if self.incarceration is None:
                validation_errors["incarceration"] = "Incarceration must have a selected value"

    def validate_field_num_lifetime_partners(self, validation_errors):
        if hasattr(self, "num_lifetime_partners"):
            if self.num_lifetime_partners is not None:
                if self.num_lifetime_partners < 0:
                    validation_errors["num_lifetime_partners"] = "Sex partners must be greater or equal to 0"
                if self.num_lifetime_partners > 50000:
                    validation_errors["num_lifetime_partners"] = "Sex partners must be less than or equal to 50000"

    def validate_field_past_sti(self, validation_errors):
        if hasattr(self, "past_sti"):
            if self.past_sti is None:
                validation_errors["past_sti"] = "Past STI must have a selected value"

    def validate_field_pregnant(self, validation_errors):
        if hasattr(self, "pregnant"):
            if self.pregnant is None:
                validation_errors["pregnant"] = "Pregnant must have a selected value"

    def validate_field_sexual_abuse(self, validation_errors):
        if hasattr(self, "sexual_abuse"):
            if self.sexual_abuse is None:
                validation_errors["sexual_abuse"] = "Sexual abuse must have a selected value"

    def validate_field_tattoos(self, validation_errors):
        if hasattr(self, "tattoos"):
            if self.tattoos is None:
                validation_errors["tattoos"] = "Tattoos must have a selected value"

    def validate_field_transgender(self, validation_errors):
        if hasattr(self, "transgender"):
            if self.transgender is None:
                validation_errors["transgender"] = "Transgender must have a selected value"

#------------------------
class LivingWithCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class HousingTypeCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class ToiletLocationCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    
class FinancialSupportCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    


#------------------------  SocialHistory
class SocialHistory(TSIS2BaseModel):

    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    performed_by =  models.CharField(max_length=255, blank=True, null=True)
    facility = models.ForeignKey("Facility", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    living_with = models.ForeignKey("LivingWithCode", blank=False, null=False, related_name='socialhistory_living_with', on_delete=models.PROTECT)
    living_with_other = models.CharField(max_length=255, blank=True, null=True)
    house_type = models.ForeignKey("HousingTypeCode", blank=False, null=False, related_name='socialhistory_house_type', on_delete=models.PROTECT)
    house_type_other = models.CharField(max_length=255, blank=True, null=True)
    family_coping = models.TextField(blank=True, null=True)
    electricity = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='socialhistory_electricity', on_delete=models.PROTECT)
    water_supply = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='socialhistory_water_supply', on_delete=models.PROTECT)
    toilet = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='socialhistory_toilet', on_delete=models.PROTECT)
    toilet_location = models.ForeignKey("ToiletLocationCode", blank=False, null=False, on_delete=models.PROTECT)
    toilet_location_other = models.CharField(max_length=255, blank=True, null=True)
    children_under_15 = models.IntegerField(blank=True, null=True)
    num_persons_in_household = models.IntegerField(blank=True, null=True)
    pets_and_animals = models.CharField(max_length=255, blank=True, null=True)
    principal_caregiver = models.CharField(max_length=255, blank=True, null=True)
    hiv_status_disclosed_to = models.CharField(max_length=255, blank=True, null=True, verbose_name="HIV status disclosed to")
    financial_support = models.ForeignKey("FinancialSupportCode", blank=False, null=False, related_name='socialhistory_financial_support', on_delete=models.PROTECT)
    financial_support_other = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    overseas_travel = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='socialhistory_overseas_travel', on_delete=models.PROTECT)
    deported = models.ForeignKey("YesNoCode", blank=False, null=False, related_name='socialhistory_deported', on_delete=models.PROTECT)
    deported_country = models.CharField(max_length=255, blank=True, null=True)
    use_marijuana = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_marijuana', on_delete=models.PROTECT)
    use_marijuana_other = models.CharField(max_length=255, blank=True, null=True)
    use_alcohol = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_alcohol', on_delete=models.PROTECT)
    use_alcohol_other = models.CharField(max_length=255, blank=True, null=True)
    use_cigarettes = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_cigarettes', on_delete=models.PROTECT)
    use_cigarettes_other = models.CharField(max_length=255, blank=True, null=True)
    use_crack_cocaine = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_crack_cocaine', on_delete=models.PROTECT)
    use_crack_cocaine_other = models.CharField(max_length=255, blank=True, null=True)
    use_inhalants = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_iinhalants', on_delete=models.PROTECT)
    use_inhalants_other = models.CharField(max_length=255, blank=True, null=True)
    use_ivdu = models.ForeignKey("FrequencyCode", blank=False, null=False, verbose_name="use IVDU", related_name='socialhistory_use_ivdu', on_delete=models.PROTECT)
    use_ivdu_other = models.CharField(max_length=255, blank=True, null=True)
    use_other_substances = models.ForeignKey("FrequencyCode", blank=False, null=False, related_name='socialhistory_use_other_substances', on_delete=models.PROTECT)
    use_other_other = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        ordering = ['-date']
        verbose_name_plural = 'Social histories'

    def __str__(self):
        return "%s" % (self.date)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_date(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_date(self, validation_errors):
        if hasattr(self, "date"):
            if self.date is not None:
                if self.date > timezone.now().date():
                    validation_errors["date"] = "Date can not be set in the future"
            else:
                validation_errors["date"] = "Date can not be left blank"
#--------------------------------

class Reason_not_starting_prep(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)

# risk assessment

class RiskAssessment(TSIS2BaseModel):

    RISKS = (
    ('MSM', 'MSM'),
    ('TRANS', 'TRANS'),
    ('HRM', 'HRM'),
    ('HRF', 'HRF'),
    ('Other', 'Other'),
    )
    YES_NO = (
    ('Yes', 'Yes'),
    ('No', 'No')
    )


    CONCEIVE = (
    ('Trying to conceive', 'Trying to conceive'),
    ('Future', 'Future'),
    ('No', 'No'),
    ('Dont know', 'Don\'t know'),
    )

    IF_PREGNANT = (
    ('Planned', 'Planned'),
    ('Unplanned', 'Unplanned'),
    )

    TEST_RESULTS = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Not Done', 'Not Done'),
    )

    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    facility = models.ForeignKey("Facility", blank=False, null=False, on_delete=models.PROTECT)
    assessment_date = models.DateField(blank=False, null=False)
    performed_by = models.CharField(max_length=50, blank=True, null=True)

    #risk assessment
    risk_keypop_profile = models.CharField(max_length=255, choices = RISKS, null=True)
    sex_partner_hiv_positive = models.CharField(max_length=255, choices = YES_NO, null=True)
    sex_partner_hiv_positive_not_on_art = models.BooleanField()
    sex_partner_hiv_positive_on_art_6months = models.BooleanField()
    sex_partner_hiv_positive_suspected_poor_adherence_to_art = models.BooleanField()
    sex_partner_hiv_positive_detectable_hiv_viral_load = models.BooleanField()
    sex_partner_hiv_positive_couple_trying_to_conceive = models.BooleanField()
    sex_partner_high_risk_and_hiv_status_unknown = models.BooleanField()
    has_sex_with_multiple_partners=models.BooleanField()

    ongoing_ipv_gbv =models.BooleanField()
    transactional_sex=models.BooleanField()
    recent_sti_6months=models.BooleanField()
    recurrent_use_pep=models.BooleanField()
    recurrent_sex_under_influence_of_alcohol_drugs=models.BooleanField()
    inconsistent_or_no_condom_use=models.BooleanField()
    shared_needles_or_syringes=models.BooleanField()
    #medical assessment
    blood_pressure = models.CharField(max_length=255, blank=True, null=True)
    weight_kg =models.IntegerField(validators=[MaxValueValidator(300), MinValueValidator(20)])
    height_cm=models.IntegerField(validators=[MaxValueValidator(220), MinValueValidator(20)])
    signs_of_sti = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_signs_of_sti')

    liver_disease_treatment = models.CharField(max_length=255, blank=False, null=False)
    kidney_disease_treatment= models.CharField(max_length=255, blank=False, null=False)
    chronic_illness_other= models.CharField(max_length=255, blank=False, null=False)
    male_circumcised = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_male_circumcised')

    lmp_date = models.DateField(blank=True, null=True)
    pregnant = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_pregnant')
    if_pregnant  = models.CharField(max_length=255, blank=False, null=False, choices=IF_PREGNANT)

    breast_feeding  = models.ForeignKey("YesNoCode", blank=False, null=False,  on_delete=models.PROTECT,  related_name='risk_assessment_breast_feeding')

    family_planning_female = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_family_planning_female')

    plan_to_have_children  = models.CharField(max_length=255, blank=False, null=False, choices=CONCEIVE)

    clinical_notes = models.TextField(blank=True, null=True)

#rep Initiation
    hepatitis_b_results = models.CharField(max_length=50, blank=False, null=False, choices=TEST_RESULTS)
    hepatitis_c_results = models.CharField(max_length=50, blank=False, null=False, choices=TEST_RESULTS)
    serum_creatinine = models.CharField(max_length=50, blank=False, null=False, choices=TEST_RESULTS)
    serum_creatinine_result = models.CharField(max_length=50, blank=False, null=False,  default=0)

    prep_initiation_additional_steps = models.TextField(blank=True, null=True)
    
    previous_prep_use = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_previous_prep_use')
    condoms_issued = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_condoms_issued')
    willing_to_start_prep = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_willing_to_start_prep')
    adherence_counseling_done = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_adherence_counseling_done')

    reason_not_will_to_start_prep =  models.ForeignKey("Reason_not_starting_prep", blank=False, null=False,  on_delete=models.PROTECT)
   
    signs_of_acute_hiv = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_signs_of_acute_hiv')
    medically_ineligible_to_start_prep = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_medically_ineligible_to_start_prep')
    contraindications_for_TDF_FTC_TDF_3TC_TDF = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_contraindications_for_TDF_FTC_TDF_3TC_TDF')
    prescribed_prep_at_initial_visit = models.ForeignKey("YesNoCode", blank=False, null=False, on_delete=models.PROTECT, related_name='risk_assessment_prescribed_prep_at_initial_visit')
    prescribed_prep_at_initial_visit_regime = models.ForeignKey("Regimen", blank=False, null=False, on_delete=models.PROTECT)
    prescribed_prep_at_initial_visit_regime_months_duration = models.ForeignKey("MonthDurationCode", blank=False, null=False, on_delete=models.PROTECT) 
    prescribed_prep_at_initial_visit_date_of_initiation = models.DateField(blank=True, null=True)
   
    def __str__(self):
        return "%s" % self.assessment_date

   # risk assessment end


# prep eligibility

class PrepEligibility(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    facility = models.ForeignKey("Facility", blank=False, null=False, on_delete=models.PROTECT)
    assessment_date = models.DateField(blank=False, null=False)
    performed_by = models.CharField(max_length=50, blank=True, null=True)

    hiv_negative = models.BooleanField(default=False)
    substantial_hiv_risk = models.BooleanField(default=False)
    no_signs_of_acute_hiv = models.BooleanField(default=False)
    has_creatinine_clearance_eGFR_over_60_ml_min = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.assessment_date
    
# end prep eligibility




class SexualHistory(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    interview_date = models.DateField(blank=False, null=False)
    last_sexual_encounter = models.DateField(blank=True, null=True)
    lmp_date = models.DateField(blank=True, null=True)
    gender_last_sex_partner = models.CharField(blank=True, null=True, max_length=30, choices=Sex_Partner_Gender )
    gender_based_violence = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='gender_violence_set')
    intimate_partner_violence = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='partner_violence_set')

    hiv_status_sex_partner = models.CharField(blank=True, null=True, max_length=30, choices=HIV_Result )

    no_sex_partners_last_month = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]    )
    
    no_sex_partners_last_3month = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5000)]    )
    
    no_sex_partners_last_12month = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)]   )
    

    gender_of_sex_partners_past_12months = models.CharField(max_length=30,choices=Sex_Partner_Gender)
    condom_use_last_3months = models.CharField(max_length=30, choices = CONDOM_USE)
    anal_sex_in_last_12_months = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='anal_sex_in_12months_set')
    anal_receptive = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='anal_receptive_set')
    anal_insertive = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='anal_insertive_set')
    circumcised = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='circumcised_set')
    in_your_lifetime_ever_paid_for_sex = models.ForeignKey("YesNoCode", on_delete=models.CASCADE,related_name='paid_for_sex_set')
    is_sex_in_exchange_for_money_a_source_of_income_for_you = models.ForeignKey("YesNoCode", on_delete=models.CASCADE,related_name='sex_for_money_income_set')
    condom_use_last_sex_encounter = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='condom_use_last_sex_set')
    condom_use_last_anal_sex_encounter = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='condom_use_last_anal_sex_set')
    previous_hiv_test = models.ForeignKey("YesNoCode", on_delete=models.CASCADE,  related_name='previous_hiv_test_set')
    contraception = models.ForeignKey("ContraceptiveMethodCode", blank=False, null=False, on_delete=models.PROTECT)
    previous_prep_use = models.ForeignKey("YesNoCode", on_delete=models.CASCADE, related_name='previous_prep_use_set')

    notes = models.TextField(blank=True, null=True)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)


    def __str__(self):
        return "%s %s" % (self.client, self.date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

# -----------------------

class Docket_new(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    docket_no  = models.CharField(blank=False, null=False, max_length=30)
    date_created = models.DateField(blank=False, null=False)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
            return "%s %s" % (self.facility, self.docket_no)
    

class OutOfCareStatus(TSIS2BaseModel):
    status_date = models.DateField(blank=False, null=False)
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    reason  = models.ForeignKey("outofcarestatuscode", blank=False, null=False, on_delete=models.PROTECT)
   
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
            return "%s %s" % (self.facility, self.reason)


class OutOfCareStatusCode(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)


class Liver_Kidney_Tests(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    test_name  = models.ForeignKey("liver_kidney_code", blank=False, null=False, on_delete=models.PROTECT)
    test_date = models.DateField(blank=False, null=False)
    test_results = models.CharField(max_length=50, blank=False, null=False)
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
            return "%s %s" % (self.test_name, self.test_results)
    
class Liver_Kidney_Code(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    

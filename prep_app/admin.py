from django.contrib import admin
import inspect
from .models import Client, ARVMedication, Address, GenderCode, MaritalStatusCode, RegionCode, RegimenLineCode, CommunityCode, Parish, Regimen, MonthDurationCode, CD4Count, ViralLoad, YesNoCode, OtherLab, EmergencyContact, RelationshipCode, Facility
from .models import Organization, HivCategoryCode, RespiratoryRateCode, PapSmearResultCode, MammogramResultCode, UrinalysisCode, TreponemalResultCode, NonTreponemalResultCode, FamilyPlanningMethodCode, PatientStabilityStatusCode
from .models import LabTestCode, PhysicalExam, PrepStatus, PrepStatusDetail, UserFacilityAssignment,  SocialHistory, RiskHistory, EmergencyContact, STI_TestCodes, STI_Results, STI_TestsDone, STI_Treatment, RiskAssessment, Reason_not_starting_prep, SexualHistory, Docket_new
from .models import OutOfCareStatus, OutOfCareStatusCode, Liver_Kidney_Tests, Liver_Kidney_Code

from django.contrib.auth.admin import UserAdmin

class UserFacilityAssignmentInline(admin.TabularInline):
    model = UserFacilityAssignment
    extra = 1  # Number of empty forms to display

class CustomUserAdmin(UserAdmin):
    inlines = [UserFacilityAssignmentInline]


admin.site.register(Liver_Kidney_Tests)
admin.site.register(Liver_Kidney_Code)

admin.site.register(OutOfCareStatusCode)
admin.site.register(OutOfCareStatus)
admin.site.register(Docket_new)
admin.site.register(SexualHistory)
admin.site.register(Reason_not_starting_prep)
admin.site.register(RiskAssessment)
admin.site.register(STI_Treatment)
admin.site.register(STI_TestsDone)
admin.site.register(STI_Results)
admin.site.register(STI_TestCodes)

admin.site.register(RiskHistory)
admin.site.register(SocialHistory)




admin.site.register(UserFacilityAssignment)


admin.site.register(PrepStatus)
admin.site.register(PrepStatusDetail)

admin.site.register(Client)
admin.site.register(ARVMedication)
admin.site.register(Address)
admin.site.register(GenderCode)
admin.site.register(MaritalStatusCode)
admin.site.register(RegionCode)
admin.site.register(RegimenLineCode)
admin.site.register(Regimen)
admin.site.register(CommunityCode)
admin.site.register(Parish)
admin.site.register(MonthDurationCode)
admin.site.register(CD4Count)
admin.site.register(ViralLoad)
admin.site.register(YesNoCode)
admin.site.register(OtherLab)
admin.site.register(EmergencyContact)
admin.site.register(RelationshipCode)
admin.site.register(Facility)
admin.site.register(LabTestCode)
admin.site.register(Organization)

admin.site.register(HivCategoryCode)
admin.site.register(RespiratoryRateCode)
admin.site.register(PapSmearResultCode)
admin.site.register(MammogramResultCode)
admin.site.register(UrinalysisCode)
admin.site.register(TreponemalResultCode)
admin.site.register(NonTreponemalResultCode)
admin.site.register(FamilyPlanningMethodCode)
admin.site.register(PatientStabilityStatusCode)
admin.site.register(PhysicalExam)

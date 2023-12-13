import django
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

from django.db import models

soft_delete_executed = django.dispatch.Signal()


class TSIS2BaseQuerySet(QuerySet):
    def delete(self):
        return super(TSIS2BaseQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(TSIS2BaseQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class TSIS2BaseModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.include_deleted = kwargs.pop('include_deleted', False)
        super(TSIS2BaseModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.include_deleted:
            return TSIS2BaseQuerySet(self.model)

        return TSIS2BaseQuerySet(self.model).filter(deleted_at=None)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class TSIS2BaseModel(models.Model):
    #facility = models.ForeignKey("Facility", on_delete=models.CASCADE)
    #facility_temp = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   related_name="%(app_label)s_%(class)s_created_by",
                                   related_query_name="%(app_label)s_%(class)ss",
                                   on_delete=models.PROTECT)
    modified_by = models.ForeignKey(User, blank=True, null=True,
                                    related_name="%(app_label)s_%(class)s_modified_by",
                                    related_query_name="%(app_label)s_%(class)ss",
                                    on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, blank=True, null=True,
                                    related_name="%(app_label)s_%(class)s_deleted_by",
                                    related_query_name="%(app_label)s_%(class)ss",
                                    on_delete=models.PROTECT)
    objects = TSIS2BaseModelManager()
    all_objects = TSIS2BaseModelManager(include_deleted=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(TSIS2BaseModelManager, self).delete()

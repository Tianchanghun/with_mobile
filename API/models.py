from django.db import models
from django.utils import timezone

# Create your models here.

class api_list(models.Model):
    api_name = models.CharField(max_length=50, blank=True, null=True)
    api_site_name = models.CharField(max_length=50, blank=True, null=True)
    api_code = models.CharField(max_length=50, blank=True, null=True)
    api_site_address = models.CharField(max_length=100, blank=True, null=True)
    api_site_url = models.CharField(max_length=100, blank=True, null=True)
    api_1_key = models.CharField(max_length=150, blank=True, null=True)
    api_2_key = models.CharField(max_length=150, blank=True, null=True)
    api_3_key = models.CharField(max_length=150, blank=True, null=True)
    api_4_key = models.CharField(max_length=150, blank=True, null=True)
    api_5_key = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

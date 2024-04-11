from django.db import models
from clients.models import Client

class ScormAsset(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)  
    duration = models.CharField(max_length=50, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    access_validity_period = models.IntegerField(default=365, blank=True)  
    license_seats = models.IntegerField(blank=True, null=True) 
    is_deleted = models.BooleanField(default=False)
    scorm_id = models.IntegerField(unique=True) 
    clients = models.ManyToManyField(Client) 
    scorm_file = models.FileField(upload_to='scorm_uploads/')
from django.db import models
from clients.models import Client

class ScormAsset(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    duration = models.DurationField(blank=True, null=True)  
    upload_date = models.DateTimeField(auto_now_add=True)
    access_validity_period = models.IntegerField(default=365, blank=True)  
    license_seats = models.IntegerField(blank=True, null=True) 
    is_deleted = models.BooleanField(default=False)
    scorm_id = models.IntegerField(unique=True, null=True)    
    clients = models.ManyToManyField(Client) 
    scorm_file = models.FileField(upload_to='scorm_uploads_zipped/')

class ScormResponse(models.Model):
    asset = models.OneToOneField(ScormAsset, on_delete=models.CASCADE, related_name='response')
    status = models.BooleanField(null=True)
    message = models.TextField(null=True)
    scormdir = models.TextField(null=True)
    full_path_name = models.TextField(null=True)
    size = models.BigIntegerField(null=True)
    zippath = models.TextField(null=True)
    zipfilename = models.TextField(null=True)
    extension = models.CharField(max_length=10, null=True)
    filename = models.TextField(null=True)
    reference = models.TextField(null=True)
    scorm = models.CharField(max_length=50, null=True)

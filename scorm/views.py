import os
import zipfile
from django.shortcuts import render, redirect
from django.conf import settings  
from .forms import ScormUploadForm
from .models import ScormAsset

def upload_scorm_view(request):
    if request.method == 'POST':
        form = ScormUploadForm(request.POST, request.FILES)
        if form.is_valid():
            scorm_file = request.FILES['scorm_file']
            # Save to the filesystem
            file_path = os.path.join(settings.MEDIA_ROOT, 'scorm_uploads', scorm_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in scorm_file.chunks():
                    destination.write(chunk)

            # Extract the ZIP file (basic, no validation here)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(settings.MEDIA_ROOT, 'scorm_uploads'))

            # Create ScormAsset database entry
            asset = ScormAsset.objects.create(
                title=os.path.splitext(scorm_file.name)[0],  # Extract basic title
                scorm_file=scorm_file
            )
            return redirect('scorm-dashboard')  
    else:
        form = ScormUploadForm()
    return render(request, 'scorm/upload_scorm.html', {'form': form})
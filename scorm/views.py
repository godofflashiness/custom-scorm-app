import json
import logging
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
import requests

from .forms import ScormUploadForm
from .models import ScormAsset, ScormResponse

logger = logging.getLogger(__name__)

@login_required
def upload_scorm_view(request):
    """
    View function for uploading a SCORM file.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Exception: If an error occurs during the file upload process.
    """
    form = ScormUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            asset = form.save(commit=False)
            try:
                scorm_file = request.FILES['scorm_file']

                headers = {
                    'Authorization': f'Bearer {settings.API_TOKEN}',
                }

                data = {
                    'file': scorm_file,
                }

                response = requests.post(settings.API_URL, headers=headers, files=data)

                if response.headers['content-type'] == 'application/json':
                    logger.debug('Response: %s', json.dumps(response.json(), indent=4))
                else:
                    logger.debug('Response: %s', response.content)

                if response.status_code == 200:
                    logger.info('File uploaded successfully')

                    response_data = response.json()

                    asset.scorm_id = int(response_data.get('scorm'))

                    asset.save() 

                    ScormResponse.objects.create(
                        asset=asset,
                        status=response_data.get('status'),
                        message=response_data.get('message'),
                        scormdir=response_data.get('scormdir'),
                        full_path_name=response_data.get('full_path_name'),
                        size=response_data.get('size'),
                        zippath=response_data.get('zippath'),
                        zipfilename=response_data.get('zipfilename'),
                        extension=response_data.get('extension'),
                        filename=response_data.get('filename'),
                        reference=response_data.get('reference'),
                        scorm=response_data.get('scorm'),
                    )
                else:
                    logger.error('Failed to upload file. Status code: %s', response.status_code)
                    logger.error('Response: %s', response.text)

                return redirect('scorm-dashboard')  
            except Exception as e:
                logger.exception('An error occurred:')
        else:
            logger.debug('Form errors: %s', form.errors.as_json())
    return render(request, 'scorm/upload_scorm.html', {'form': form})

def scorm_dashboard_view(request):
    """
    Renders the SCORM dashboard view.

    This view requires the user to be authenticated. If the user is not authenticated,
    they will be redirected to the admin login page.

    The function fetches all SCORM assets from the database and renders the 'scorm-dashboard.html'
    template with the fetched SCORM assets.

    Returns:
        A rendered HTML response containing the SCORM dashboard view.

    Raises:
        ObjectDoesNotExist: If there is an error fetching the SCORM assets from the database.
    """
    if not request.user.is_authenticated:
        return redirect('admin-login')
    
    try:
        scorms = ScormAsset.objects.all()
    except ObjectDoesNotExist:
        messages.error(request, "Error fetching scorms")
        scorms = None
    return render(request, 'scorm/scorm-dashboard.html', {'scorms': scorms})
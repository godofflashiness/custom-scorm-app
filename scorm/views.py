import json
import logging
import os


from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
import requests

from .forms import ScormUploadForm, AssignSCORMForm
from .models import ScormAsset, ScormResponse, ScormAssignment
from clients.models import Client

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

                # Check if the response has a 'content-type' header
                content_type = response.headers.get('content-type')
                if content_type == 'application/json':
                    try:
                        response_data = response.json()
                        logger.debug('Response: %s', json.dumps(response_data, indent=4))
                    except json.JSONDecodeError:
                        logger.error('Error decoding JSON from response')
                        response_data = None
                else:
                    logger.debug('Response: %s', response.content)
                    response_data = None

                if response.status_code == 200 and response_data is not None:
                    logger.info('File uploaded successfully')

                    scorm_id = response_data.get('scorm')
                    if scorm_id is not None:
                        asset.scorm_id = int(scorm_id)
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
                    if response_data is not None:
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


def assign_scorm(request, client_id):
    if request.method == 'POST':
        form = AssignSCORMForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.client_id = client_id
            assignment.save()
            return JsonResponse({'success': True})
    else:
        form = AssignSCORMForm()
    return render(request, 'clients/client_details.html', {'form': form})
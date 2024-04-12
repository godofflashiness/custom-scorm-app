from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientCreationForm, ClientUpdateForm
from .models import Client

def create_client_view(request):
    """
    View function for creating a client.

    This view function handles the creation of a client. It checks if the user is an admin,
    validates the form data, saves the client, and redirects to the client dashboard.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if not request.user.is_admin:
        return redirect('client-dashboard')  
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.errors)
            form.save() 
            print(form.errors) 
            messages.success(request, "Client created successfully")
            return redirect('client-dashboard')  
    else:
        form = ClientCreationForm()
    return render(request, 'clients/create_client.html', {'form': form})

def client_dashboard_view(request):
    """
    View function for the client dashboard.

    This view displays the client dashboard page, which shows a list of all clients.
    Only authenticated users can access this page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.

    Raises:
        None

    """
    if not request.user.is_authenticated:
        return redirect('admin-login')
    
    try:
        clients = Client.objects.all()
    except ObjectDoesNotExist:
        messages.error(request, "Error fetching clients")
        clients = None
    
    return render(request, 'clients/client_dashboard.html', {'clients': clients})


def client_update_view(request, client_id):
    """
    Update the client information.

    Args:
        request (HttpRequest): The HTTP request object.
        client_id (int): The ID of the client to update.

    Returns:
        HttpResponse: The HTTP response.

    Raises:
        Http404: If the client with the specified ID does not exist.

    """
    if not request.user.is_admin:
        return redirect('client-dashboard')

    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        if 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':  # Handle AJAX form submission
            form = ClientUpdateForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:  
            form = ClientUpdateForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, "Client updated successfully")
                return redirect('client-dashboard')
    else:  
        form = ClientUpdateForm(instance=client)

    return render(request, 'clients/client_dashboard.html', {'form': form})

def get_client_details(request, client_id):
    """
    Retrieve the details of a client based on the provided client_id.

    Args:
        request (HttpRequest): The HTTP request object.
        client_id (int): The ID of the client to retrieve details for.

    Returns:
        JsonResponse: A JSON response containing the client details.

    Raises:
        Client.DoesNotExist: If the client with the provided client_id does not exist.
    """
    client = Client.objects.get(pk=client_id)
    data = {
        'first_name': client.first_name,
        'last_name': client.last_name,
        'company': client.company,
        'contact_email': client.contact_email,
        'contact_phone': client.contact_phone,
    }
    return JsonResponse(data)

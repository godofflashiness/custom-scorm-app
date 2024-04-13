from django.db import models
from django.conf import settings


class Client(models.Model):
    """
    Represents a client in the system.

    Attributes:
        first_name (str): The first name of the client.
        last_name (str): The last name of the client.
        email (str): The email address of the client.
        contact_phone (str, optional): The phone number of the client. Can be null or blank.
        company (str): The company name of the client.
        created_at (datetime): The date and time when the client was created.
        scorm_count (int): The number of SCORM objects associated with the client.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

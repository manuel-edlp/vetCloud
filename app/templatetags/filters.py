# filters.py
from django import template
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from django.conf import settings
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def generate_sas_token(image_url):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_BLOB_CONNECTION_STRING)
    container_name = settings.AZURE_BLOB_CONTAINER_NAME
    blob_name = image_url.split("/")[-1]
    
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # Expira en una hora
    )
    # prueba
    return f"?{sas_token}"

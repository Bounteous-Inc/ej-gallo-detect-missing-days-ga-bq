import os
import json
from google.cloud import secretmanager

def access_secret_version(project_secret_id, secret_name, version_id):
    """
    Get a secret value from GCP Secret Manager
    :param project_secret_id: (str) Numeric ID pulled from secret
    :param secret_name: (str) Name of secret
    :param version_id: (str) version number or 'latest'
    :return: (str) Full Secret Payload
    """

    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version. Access the secret version.
    name = f"projects/{project_secret_id}/secrets/{secret_name}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    response_str = response.payload.data.decode("UTF-8")
    response_dict = json.loads(response_str)

    return response_dict

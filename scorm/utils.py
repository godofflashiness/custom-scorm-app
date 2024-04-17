import bsdiff4
import os
import tempfile
import zipfile
import logging

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

key = Fernet.generate_key()

def encrypt_data(client_id, scorm):
    cipher_suite = Fernet(key)
    data = (str(client_id) + '-' + str(scorm)).encode()
    cipher_text = cipher_suite.encrypt(data)
    return cipher_text.decode() 

def decrypt_data(cipher_text):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text.encode())
    return plain_text.decode()

def replace_placeholders(file_path, client_specific_data):
    logger.info(f"Opening file: {file_path}")
    with open(file_path, 'r+') as file:
        contents = file.read()
        logger.info(f"Before replacement:\n{contents}")  # Log the contents before replacement
        if 'configuration.js' in file_path:
            logger.info("Replacing 'ID' in configuration.js")
            contents = contents.replace('ID', client_specific_data['id'], 1)
        elif 'imsmanifest.xml' in file_path:
            logger.info("Replacing '{{SCORM_TITLE}}' in imsmanifest.xml")
            contents = contents.replace('{{SCORM_TITLE}}', client_specific_data['scorm_title'])
        logger.info(f"After replacement:\n{contents}")  # Log the contents after replacement
        file.seek(0)
        file.write(contents)
        file.truncate()

def generate_client_scorm_file(original_scorm_file, client_specific_data):
    logger.info("Creating temporary directory")
    temp_dir = tempfile.mkdtemp()
    logger.info(f"Extracting {original_scorm_file.path} to {temp_dir}")
    with zipfile.ZipFile(original_scorm_file.path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    replace_placeholders(os.path.join(temp_dir, 'imsmanifest.xml'), client_specific_data)
    replace_placeholders(os.path.join(temp_dir, 'configuration.js'), client_specific_data)
    client_scorm_file_path = tempfile.mktemp()
    logger.info(f"Creating client SCORM file at: {client_scorm_file_path}")
    with zipfile.ZipFile(client_scorm_file_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))
    logger.info(f"Client SCORM file generated at: {client_scorm_file_path}")
    return client_scorm_file_path
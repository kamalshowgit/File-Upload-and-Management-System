# views.py

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import os
from django.shortcuts import render
from openpyxl import load_workbook
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# def file_upload_view(request):
#     if request.method == 'POST' and request.FILES['file']:
#         # Save the uploaded file to the "uploaded_files" folder
#         file = request.FILES['file']
#         fs = FileSystemStorage()
#         filename = fs.save(os.path.join('uploaded_files', file.name), file)
#         return render(request, 'uploaded.html')
#     return render(request, 'upload.html')


def file_upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        # Save the uploaded file to the "uploaded_files" folder
        file = request.FILES['file']
        fs = FileSystemStorage()

        # Check if a file with the same name already exists
        name, extension = os.path.splitext(file.name)
        counter = 0
        while fs.exists(os.path.join('uploaded_files', file.name)):
            counter += 1
            file.name = f"{name}_{counter}{extension}"
            
        # Save the file to the file system
        filename = fs.save(os.path.join('uploaded_files', file.name), file)
        return render(request, 'uploaded.html')
    return render(request, 'upload.html')


def admin_panel(request):
    # Path to the directory where uploaded files are stored
    uploaded_files_dir = os.path.join(settings.BASE_DIR, 'uploaded_files')
    # Get a list of all files in the directory
    files = os.listdir(uploaded_files_dir)
    # Create a list of dictionaries containing file name and path
    file_list = []
    for file in files:
        file_path = os.path.join(uploaded_files_dir, file)
        file_list.append({'name': file, 'path': file_path})
    # Render the admin panel template with the file list
    return render(request, 'admin_panel.html', {'files': file_list})
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os

def view_file(request, file_name):
    # Provide the correct path to the directory where your files are stored
    file_directory = '/path/to/files/directory'
    file_path = os.path.join(file_directory, file_name)

    if os.path.exists(file_path):
        # If the file exists, determine whether to show or download it based on the request type
        if request.GET.get('download'):
            # If the request contains a 'download' parameter, initiate file download
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
        else:
            # Otherwise, show the file in the browser
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=' + file_name
                return response
    else:
        # Handle the case when the file doesn't exist
        return HttpResponse("File not found.")

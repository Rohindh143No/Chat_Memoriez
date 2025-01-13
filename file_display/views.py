# file_display/views.py
import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings

# View to list chat files (HTML and TXT) from the media directory
def display_chat_file_list(request):
    # Path to the MEDIA_ROOT directory
    media_dir = os.path.join(settings.MEDIA_ROOT,'chat_files')

    # Ensure the directory exists
    if not os.path.exists(media_dir):
        return HttpResponse('No files found', status=404)

    # List all .txt and .html files directly from the media directory
    txt_files = [f for f in os.listdir(media_dir) if f.endswith('.txt')]
    html_files = [f for f in os.listdir(media_dir) if f.endswith('.html')]

    # Render the 'elif.html' template and pass the file lists
    return render(request, 'file_display/elif.html', {
        'txt_files': txt_files,
        'html_files': html_files
    })

# View to display .txt or .html files
def display_file(request, filename):
    # Path to the MEDIA_ROOT directory
    media_dir = os.path.join(settings.MEDIA_ROOT ,'chat_files')
    file_path = os.path.join(media_dir, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404("File not found")

    # Determine the content type based on file extension
    if filename.endswith('.html'):
        content_type = "text/html"
    elif filename.endswith('.txt'):
        content_type = "text/plain"
    else:
        raise Http404("Unsupported file type")

    # Open and read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Return the file content as an HTTP response with the correct content type
    return HttpResponse(content, content_type=content_type)

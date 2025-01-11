import os
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .program import parse_chat, generate_html


# View to list chat files (HTML and TXT)
def chat_file_list(request):
    media_dir = os.path.join(settings.MEDIA_ROOT, 'chat_files')
    os.makedirs(media_dir, exist_ok=True)  # Ensure directory exists

    # List all .txt and .html files
    txt_files = [f for f in os.listdir(media_dir) if f.endswith('.txt')]
    html_files = [f for f in os.listdir(media_dir) if f.endswith('.html')]

    return render(request, 'chat/elif.html', {
        'txt_files': txt_files,
        'html_files': html_files,
    })


# View to serve individual chat files (either .txt or .html)
def chat_file_view(request, filename):
    media_dir = os.path.join(settings.MEDIA_ROOT, 'chat_files')
    file_path = os.path.join(media_dir, filename)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    content_type = "text/html" if filename.endswith('.html') else "text/plain"
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return HttpResponse(content, content_type=content_type)


# Main chat upload and analysis view
def chat_view(request):
    """if 'visitor_count' not in request.session:
        request.session['visitor_count'] = 0  # Initialize the visitor count
    request.session['visitor_count'] += 132  # Increment the count"""

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', uploaded_file.name)
        fs.save(file_path, uploaded_file)

        try:
            # Parse the chat file
            chat_data, participants, message_counts = parse_chat(file_path)

            # Generate HTML output based on parsed data
            output_html = os.path.join(settings.MEDIA_ROOT, 'chat_files', f"{participants[1]}.html")
            generate_html(chat_data, participants, message_counts, output_html)

            # Provide the URL to the generated HTML file
            html_file_url = os.path.join(settings.MEDIA_URL, 'chat_files', f"{participants[1]}.html")

            return render(request, 'chat/chat.html', {
                'html_file_url': html_file_url,
                'participants': participants,
                'message_counts': message_counts,
                'participant_0': participants[0],  # Participant 0
                'participant_1': participants[1],  # Participant 1
                'participant_0_count': message_counts.get(participants[0], 0),  # Participant 0 count
                'participant_1_count': message_counts.get(participants[1], 0),  # Participant 1 count
                'visitor_count': request.session['visitor_count'],  # Pass the visitor count to the template
            })
        except Exception as e:
            return render(request, 'chat/chat.html', {'error': f"Error processing file: {str(e)}"})

    return render(request, 'chat/chat.html', {'visitor_count': request.session['visitor_count']})


# View to handle file download
def download_chat(request, participant):
    file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', f"{participant}.html")

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{participant}.html')
        return response
    else:
        return render(request, 'chat/chat.html', {'error': 'File not found.'})


# View to display the generated chat HTML file
def view_chat(request, participant):
    if not participant:
        return render(request, 'chat/chat.html', {'error': 'Participant not specified.'})

    file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', f"{participant}.html")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return render(request, 'chat/view_chat.html', {'content': content})
    else:
        return render(request, 'chat/chat.html', {'error': 'File not found.'})

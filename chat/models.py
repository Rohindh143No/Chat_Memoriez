from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Files will be stored in the 'uploads/' folder inside MEDIA_ROOT
    file_name = models.CharField(max_length=255)   # Storing the name of the file (optional)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date and time of file upload

    def __str__(self):
        return self.file_name
    
class ChatFile(models.Model):
    file = models.FileField(upload_to='chat_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatFile {self.id} - {self.file.name}"

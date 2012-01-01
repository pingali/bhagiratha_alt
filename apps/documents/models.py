from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime

class Document(models.Model): 
    user = models.ForeignKey(User)    
    body = models.TextField(verbose_name="Text", 
                            default="",
                            help_text="Text to be translated")
    url = models.CharField(max_length=256, 
                           verbose_name="URL",
                           null=True,
                           blank=True,
                           default=""
                           )
    
    created_at = models.DateTimeField(null=False) 
    updated_at = models.DateTimeField(null=False) 

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = datetime.today()
        self.updated_at = datetime.today()
        super(Document, self).save(*args, **kwargs)

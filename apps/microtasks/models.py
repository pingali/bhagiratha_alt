from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from bhagirath.apps.documents.models import Document 
#from bhagirath.apps.languages.models import Language 

class Microtask(models.Model): 
    user = models.ForeignKey(User)    
    document = models.ForeignKey(Document, null=True) 
    #language = models.ForeignKey(Language) 
    snippet = models.TextField(verbose_name="Snippet for Translation", 
                               default="",
                               help_text="Text to be translated")
    translation = models.TextField(verbose_name="Translation", 
                                   default="",
                                   help_text="Translation provided")
    context = models.TextField(verbose_name="Context", 
                               default="",
                               help_text="Context for Microtask")
    
    created_at = models.DateTimeField(null=False) 
    updated_at = models.DateTimeField(null=False) 

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = datetime.today()
        self.updated_at = datetime.today()
        super(Microtask, self).save(*args, **kwargs)

    

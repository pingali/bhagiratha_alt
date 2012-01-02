from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from bhagirath.apps.documents.models import Document 
from bhagirath.apps.microtasks.models import Microtask 

class Language(models.Model): 
    language = models.TextField(verbose_name="Language name", 
                                default="",
                                help_text="Target language")
    region = models.TextField(verbose_name="Prevalence region", 
                              default="",
                              help_text="Region where the language is spoken")

    @staticmethod
    def hindi():
        return Language.objects.get(language="Hindi")
        
    
class Translation(models.Model): 
    
    user = models.ForeignKey(User)    
    document = models.ForeignKey(Document, null=True) 
    microtask = models.ForeignKey(Microtask, null=True, related_name="microtask") 
    language = models.ForeignKey(Language, null=True) 
    iteration = models.IntegerField(verbose_name="Translation iteration", 
                                    default=0,
                                    help_text="Translation iteration")

    translation = models.TextField(verbose_name="Translation", 
                                   default="",
                                   help_text="Translation provided")
    status = models.TextField(verbose_name="Translation status",
                              default="init") 
    created_at = models.DateTimeField(null=False) 
    updated_at = models.DateTimeField(null=False) 

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = datetime.today()
        self.updated_at = datetime.today()
        super(Translation, self).save(*args, **kwargs)

    

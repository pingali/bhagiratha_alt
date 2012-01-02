from django import forms
from django.conf import settings 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TranslationForm
from .models import Translation, Language
import simplejson as json
import logging
import traceback 
import random 

log = logging.getLogger("translations.views")

def index(request):
    translations = Translation.objects.all() 
    template = { 'translations': translations} 
    return render_to_response(
        'translations/index.html', 
        template, 
        RequestContext(request))

def languages(request):
    languages = Language.objects.all() 
    template = { 'languages': languages} 
    return render_to_response(
        'translations/languages.html', 
        template, 
        RequestContext(request))

@login_required
def show(request, translation_id):
    print "translation_show" 
    user = request.user 
    try: 
        translation = Translation.objects.get(id=translation_id)
    except: 
        messages.error(request, "Translation does not exist")
        return HttpResponseRedirect("/translations/") 
        
    template = {"translation": translation}
    return render_to_response(
        'translations/show.html', 
        template, 
        RequestContext(request))

@login_required
def edit(request, translation_id):
    
    user = request.user 
    try: 
        instance=Translation.objects.get(id=translation_id)
    except: 
        messages.error(request, "Translation does not exist")
        return HttpResponseRedirect("/translations") 

    if request.method == "POST":
        print "received post", request.POST 
        print request.POST
        form = TranslationForm(data=request.POST, instance=instance)
        if form.is_valid():
            try: 
                translation = form.save(commit=False) 
                translation.user = request.user 
                translation.save() 
                messages.success(request, "Translation saved!")
                return HttpResponseRedirect("/translations/") 
            except: 
                log.exception("Translation saving failed")
                traceback.print_exc() 
                messages.error(request, "Translation saving failed")
            
        #else:
        #    messages.error(request, form.errors)

    else:
        print "Received a GET" 
        try: 
            form = TranslationForm(instance=instance)
        except: 
            form = TranslationForm()
            
    template = {"form":form}
    return render_to_response(
        'translations/edit.html', 
        template, 
        RequestContext(request))



@login_required
def reassign(request, translation_id):
    try: 
        t = Translation.objects.get(pk=translation_id)
    except: 
        messages.error(request, "Could not find the Snippet specified") 
        return HttpResponseRedirect("/translations/")
    
    try: 
        users = User.objects.all() 
        max_num = len(users)
        user = users[random.randint(0, max_num-1)]
        translation.user = user 
        messages.success(request, "Reassigned request to %s " % user.username)
    except: 
        log.exception("Unable to reassign!") 
        messages.error(request, "Unable to reassign. " + 
                       "Please contact administrator!") 
        pass 

    return HttpResponseRedirect("/translations/show/%d" % int(translation_id))


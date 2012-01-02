from django import forms
from django.conf import settings 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import MicrotaskForm
from .models import Microtask
import simplejson as json
import logging
import traceback 
import random 

log = logging.getLogger("microtasks.views")

def index(request):
    mtasks = Microtask.objects.all() 
    template = { 'mtasks': mtasks} 
    return render_to_response(
        'microtasks/index.html', 
        template, 
        RequestContext(request))

@login_required
def show(request, mtask_id):
    print "mtask_show" 
    user = request.user 
    try: 
        mtask = Microtask.objects.get(id=mtask_id)
    except: 
        messages.error(request, "Microtask does not exist")
        return HttpResponseRedirect("/microtasks/") 
        
    template = {"mtask": mtask}
    return render_to_response(
        'microtasks/show.html', 
        template, 
        RequestContext(request))

@login_required
def edit(request, mtask_id):
    
    user = request.user 
    try: 
        instance=Microtask.objects.get(id=mtask_id)
    except: 
        messages.error(request, "Microtask does not exist")
        return HttpResponseRedirect("/microtasks") 

    if request.method == "POST":
        print "received post", request.POST 
        print request.POST
        form = MicrotaskForm(data=request.POST, instance=instance)
        if form.is_valid():
            try: 
                mtask = form.save(commit=False) 
                mtask.user = request.user 
                mtask.save() 
                messages.success(request, "Microtask saved!")
                return HttpResponseRedirect("/microtasks/") 
            except: 
                log.exception("Microtask saving failed")
                traceback.print_exc() 
                messages.error(request, "Microtask saving failed")
            
        #else:
        #    messages.error(request, form.errors)

    else:
        print "Received a GET" 
        try: 
            form = MicrotaskForm(instance=instance)
        except: 
            form = MicrotaskForm()
            
    template = {"form":form}
    return render_to_response(
        'microtasks/edit.html', 
        template, 
        RequestContext(request))



@login_required
def reassign(request, mtask_id):
    try: 
        d = Microtask.objects.get(pk=mtask_id)
    except: 
        messages.error(request, "Could not find the Snippet specified") 
        return HttpResponseRedirect("/microtasks/")
    
    try: 
        mtask = Microtask.objects.filter(pk=mtask_id)
        users = User.objects.all() 
        max_num = len(users)
        user = users[random.randint(0, max_num-1)]
        mtask.user = user 
        messages.success(request, "Reassigned request to %s " % user.username)
    except: 
        log.exception("Unable to reassign!") 
        messages.error(request, "Unable to reassign. " + 
                       "Please contact administrator!") 
        pass 

    return HttpResponseRedirect("/microtasks/show/%d" % int(mtask_id))

@login_required
def assign(request, doc_id):
    try: 
        assign_roundrobin(request, doc_id) 
    except: 
        log.exception("Found some error!") 
        messages.error(request, "Found some error!") 
        pass 

    return HttpResponseRedirect("/documents/show/%d" % int(doc_id))

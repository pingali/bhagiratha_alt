from django import forms
from django.conf import settings 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
from bhagirath.apps.microtasks.models import Microtask 
import simplejson as json
import logging
import traceback 

log = logging.getLogger("documents.views")

def index(request):
    docs = Document.objects.all() 
    template = { 'docs': docs} 
    return render_to_response(
        'documents/index.html', 
        template, 
        RequestContext(request))

@login_required
def new(request):
    doc = Document(body="",url="", user=request.user)
    doc.save() 
    return HttpResponseRedirect("/documents/edit/%d" % doc.id) 
    
@login_required
def show(request, doc_id):
    print "document_show" 
    user = request.user 
    try: 
        doc = Document.objects.get(pk=doc_id)
    except: 
        messages.error(request, "Document does not exist")
        return HttpResponseRedirect("/documents") 

    mtasks = Microtask.objects.filter(document=doc) 
    template = {"doc": doc, "mtasks": mtasks}
    return render_to_response(
        'documents/show.html', 
        template, 
        RequestContext(request))

@login_required
def edit(request, doc_id):
    
    user = request.user 
    try: 
        instance=Document.objects.get(pk=doc_id)
    except: 
        messages.error(request, "Document does not exist")
        return HttpResponseRedirect("/documents") 

    if request.method == "POST":
        print "received post", request.POST 
        print request.POST
        form = DocumentForm(data=request.POST, instance=instance)
        if form.is_valid():
            try: 
                doc = form.save(commit=False) 
                doc.user = request.user 
                doc.save() 
                messages.success(request, "Document saved!")
                return HttpResponseRedirect("/documents") 
            except: 
                log.exception("Document saving failed")
                traceback.print_exc() 
                messages.error(request, "Document saving failed")
            
        #else:
        #    messages.error(request, form.errors)

    else:
        print "Received a GET" 
        try: 
            form = DocumentForm(instance=instance)
        except: 
            form = DocumentForm()
            
    template = {"form":form}
    return render_to_response(
        'documents/edit.html', 
        template, 
        RequestContext(request))


@login_required
def delete(request, doc_id):
    d = Document.objects.get(pk=doc_id)
    d.delete() 
    return HttpResponseRedirect("/documents/")     

def assign_roundrobin(request, doc_id):
    # Assign to all users in roundrobin fashion 
    try:
        d = Document.objects.get(pk=doc_id)
    except: 
        messages.error(request, "Could not find the document specified") 
        return 

    text = d.body 
    snippets = d.body.split(".")
    users = User.objects.all() 
    max_num = len(users)
    user_num = 0 
    for snippet in snippets: 
        m = Microtask(snippet=snippet,
                      document=d, 
                      user=users[user_num],
                      translation="",
                      context=""
                      )
        m.save() 
        user_num += 1 
        if max_num <= user_num: 
            user_num = 0 
    

@login_required
def assign(request, doc_id):
    try: 
        assign_roundrobin(request, doc_id) 
    except: 
        log.exception("Found some error!") 
        messages.error(request, "Found some error!") 
        pass 

    return HttpResponseRedirect("/documents/show/%d" % int(doc_id))

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from appt.models import TabA, TabB, TabC
def index(r):
    return HttpResponse(__file__)

def session(rq):
    """
    session of django study
    """
    rq.session['username']='wxy'
    return HttpResponse(__file__ + '::session and first user is my daugter:' + rq.session['username'])


"""
测试多对多  1个表两个foreignkey
"""

def taba(request):
    rq_method = request.method
    if rq_method == 'POST':
        # add/update to database
        o_tb = TabB.objects.get(id=1)
        o_tc = TabC.objects.all()
        o_ta = TabA.objects.create(title=request.POST['title'],
                                   content=request.POST['content'])

        o_ta.save()
        o_ta.tc = o_tc
        o_ta.tc.add()
        return HttpResponse('POST')
    elif rq_method == 'GET':
        act = 'act' in request.GET and request.GET['act'] or 'list'
        if act == 'add':

            # display form
            return render_to_response('appt/taba_add.html')
        elif act == 'del':
            # del
            pass
        else:
            # list 
            pass

def tabb(request):
    rq_method = request.method
    if rq_method == 'POST':
        # add/update to database
        o_tabb = TabB.objects.create(path=request.POST['path'],
                                     file_name=request.POST['file_name'])
        o_tabb.save()
        return HttpResponse('POST')
    elif rq_method == 'GET':
        act = 'act' in request.GET and request.GET['act'] or 'list'
        if act == 'add':

            # display form
            return render_to_response('appt/tabb_add.html')
        elif act == 'del':
            # del
            pass
        else:
            # list 
            pass


def tabc(request):
    rq_method = request.method
    if rq_method == 'POST':
        # add/update to database
        o_tabc = TabC.objects.create(utitle=request.POST['title'],
                                     ucontent=request.POST['content'])
        o_tabc.save()
        return HttpResponse('POST')
    elif rq_method == 'GET':
        act = 'act' in request.GET and request.GET['act'] or 'list'
        if act == 'add':

            # display form
            return render_to_response('appt/taba_add.html')
        elif act == 'del':
            # del
            pass
        else:
            # list 
            pass


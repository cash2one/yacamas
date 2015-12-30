from django.shortcuts import render_to_response

def main(request, action='list'):

    return render_to_response('views.group.main')

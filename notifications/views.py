from urllib.request import parse_keqv_list
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.


@login_required
def list_notifications(request):
    all_notifications = Notification.objects.filter(has_seen=False, user=request.user).order_by('-date_created')
    return render(request, 'notifications/list.html', {'notifications': all_notifications, 'notif_count': get_count(request)})


# Ajax request to delete
@login_required
def delete_notifications(request):
    if request.method == 'POST': 
        notification = Notification.objects.get(id=Notification.get_id(request.POST.get('slug')))
        notification.has_seen = True
        notification.save()
        return HttpResponse()
    else:
        return redirect('notifications:list')
    

@login_required
def get_count(request):
    all_notifications = Notification.objects.filter(has_seen=False, user=request.user)
    return all_notifications.count()
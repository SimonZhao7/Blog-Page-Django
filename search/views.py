from django.http.response import JsonResponse
from django.shortcuts import redirect
from account.models import CustomUser

# Create your views here.


def get_results(request):
    if request.method == 'POST':
        results = CustomUser.objects.filter(username__icontains=request.POST.get('search_val')).values('username', 'profile_picture')
        print(list(results))
        return JsonResponse({'results': list(results)})
    return redirect('posts:list')
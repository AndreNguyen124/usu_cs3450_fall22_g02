from .models import Profile

def getUser(request):
    if request.user.is_authenticated:
        baseUser = Profile.objects.get(id=request.user.id)
        return {'baseUser': baseUser}
    else:
        return {'baseUser': -1}



from django.views import generic
from django.shortcuts import render
from .models import Users, UsersManager


# Create your views here.
class MyListView(generic.ListView):
    paginate_by = 10
    template_name = 'feivs2019AccountManager/follower_list.html'

def getFollowers(request):
    model = Users()
    model_manager = UsersManager()
    cursor = -1
    user_model_data = []
    while cursor != 0:
        cursor = model_manager.getFollowers(cursor, user_model_data)
        for data in user_model_data :
            try:
                Users.objects.filter(pk=data['user_id']).update_or_create(**data)
            except django.db.utils.InternalError as e:
                print(e)
                pass
    #model.getFollowersStatics()
    return render(request, 'feivs2019AccountManager/follower_list.html')

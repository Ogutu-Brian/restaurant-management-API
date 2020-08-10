from user_profile.models import Profile


def get_profile_from_api_request(request):
  user = Profile.objects.get(user__username=request.user)
  return user

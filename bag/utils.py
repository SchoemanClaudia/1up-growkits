from profiles.models import UserProfile


def save_bag_on_logout(request, user):
    """
    Store current session bag to user's profile
    """
    bag = request.session.get('bag', {})
    if user.is_authenticated and bag:
        profile = UserProfile.objects.get(user=user)
        profile.saved_bag = bag
        profile.save()


def restore_bag_on_login(request, user):
    """
    Restore saved bag from profile on login
    """
    profile = UserProfile.objects.get(user=user)
    # Only restore if session bag empty
    if profile.saved_bag and not request.session.get('bag'):
        request.session['bag'] = profile.saved_bag
        profile.saved_bag = {}  # clear saved bag once restored
        profile.save()

def save_bag_on_logout(request, user):
    """ Save session bag to user's profile """
    if request.user.is_authenticated:
        profile = user.userprofile
        profile.saved_bag = request.session.get('bag', {})
        profile.save()


def restore_bag_on_login(request, user):
    """ Restore bag to session from user profile if session bag is empty """
    if user.is_authenticated:
        profile = user.userprofile
        # Only restore if session bag empty
        if not request.session.get('bag') and profile.saved_bag:
            request.session['bag'] = profile.saved_bag
            profile.saved_bag = {}
            profile.save()


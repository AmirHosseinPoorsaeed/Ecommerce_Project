from django.contrib.auth import get_user_model


User = get_user_model()


class PhoneNumberAuthBackend:
    """
    Authenticate using an phone number.
    """

    def authenticate(self, request, username=None):
        try:
            user = User.objects.get(phone_number=username)
            if user:
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

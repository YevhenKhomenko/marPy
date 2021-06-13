from django.db import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from apps_generic.whodidit.models import WhoDidIt


class UserProfile(models.Model):
    class Gender:
        male = 'm'
        female = 'f'

    GENDERS = (
        (Gender.male, 'Male'),
        (Gender.female, 'Female')
    )

    user = models.OneToOneField(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )

    date_of_birth = models.DateField(verbose_name="Date Of Birth", null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=13, null=True, blank=True)
    photo = models.ImageField(verbose_name='Profile Photo', upload_to=None, null=True, blank=True)
    bio = models.CharField(verbose_name='Profile Description', max_length=250, blank=True)
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDERS, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return 'Profile for {}'.format(self.user.email)


AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}


class UserAuthCredentials(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    is_verified = models.BooleanField(default=False)

    google_id = models.CharField(max_length=255, null=True, blank=True)
    google_access_token = models.CharField(max_length=255, null=True, blank=True)
    google_refresh_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'Auth credentials for {}'.format(self.user.email)

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


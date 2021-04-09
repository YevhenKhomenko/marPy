from django.db import models
from django.contrib.auth.models import User

from apps_generic.whodidit.models import WhoDidIt


class UserProfile(WhoDidIt):
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

    date_of_birth = models.DateField(verbose_name="Date Of Birth", default=None)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=13)
    photo = models.ImageField(verbose_name='Profile Photo', upload_to=None, blank=True)
    bio = models.CharField(verbose_name='Profile Description', max_length=250, blank=True)
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDERS, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return 'Profile for {}'.format(self.user)


class SocialTokens(models.Model):
    # TODO: implement
    pass


class RegistrationTry(models.Model):
    # TODO: implement
    pass

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ Default user profile class """

    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    user = models.OneToOneField(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
    )

    user_date_of_birth = models.DateField(default=None, verbose_name="Date Of Birth")
    user_gender = models.CharField(default=None, verbose_name='Gender', max_length=1, choices=GENDERS)
    user_phone_number = models.CharField(verbose_name='Phone Number', max_length=13)
    profile_bio = models.CharField(verbose_name='Profile Description', max_length=250)

    # TODO:from gallery app import model
    # profile_photo = models.ForeignKey(ProfilePhoto, on_delete=models.CASCADE)
    # OR
    # profile_photo = models.ImageField()

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

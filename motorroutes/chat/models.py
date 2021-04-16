from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Chat(models.Model):
    DIALOG = 'D'
    GROUP = 'G'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (GROUP, _('Group'))
    )

    type = models.CharField(
        _('Type of Chat'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Member"))

    @models.permalink
    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"))
    author = models.ForeignKey(User, verbose_name=_("Author"))
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Public Date'), default=timezone.now)
    is_readed = models.BooleanField(_('Is Readed'), default=False)
    soft_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

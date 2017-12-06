from django.conf import settings
from django.db import models

from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

# Create your models here.


class StupidCat(models.Model):
    """ For logging when a user goes somewhere they shouldn't be going """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField(max_length=16)
    requested_uri = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "timestamp"


class GlobalPerms(models.Model):
    # it's a dummy class
    class Meta:
        permissions = (
            ('search', 'Enables search functionality'),
        )


class ResizedRedirect(models.Model):
    site = models.ForeignKey(Site, verbose_name=_('site'), on_delete=models.PROTECT)
    old_path = models.CharField(
        _('redirect from'),
        max_length=190,
        db_index=True,
        help_text=_("This should be an absolute path, excluding the domain name. Example: '/events/search/'."),
    )
    new_path = models.CharField(
        _('redirect to'),
        max_length=200,
        blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL starting with 'http://'."),
    )

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        db_table = 'django_redirect2'
        unique_together = (('site', 'old_path'),)
        ordering = ('old_path',)

    def __str__(self):
        return "%s ---> %s" % (self.old_path, self.new_path)

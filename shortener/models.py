from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .baseconv import base62


class Link(models.Model):
    """
    Model that represents a shortened URL
    """
    url = models.URLField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True)


    def to_base62(self):
        return base62.from_decimal(self.id)

    def __unicode__(self):
        return  '%s : %s' % (self.to_base62(), self.url)

    class Meta:
        get_latest_by = 'date_submitted'


class Click(models.Model):
    link = models.ForeignKey(Link)
    incoming_url = models.URLField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)


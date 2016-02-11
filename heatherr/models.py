from django.db import models
from django.core.urlresolvers import reverse

import requests


class SlackAccount(models.Model):
    user = models.ForeignKey('auth.user', null=True)
    access_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255)
    incoming_webhook_url = models.CharField(max_length=255)
    incoming_webhook_channel = models.CharField(max_length=255)
    incoming_webhook_configuration_url = models.CharField(max_length=255)
    bot_user_id = models.CharField(max_length=255)
    bot_access_token = models.CharField(max_length=255)
    bot_enabled = models.BooleanField(default=False)
    bot_status = models.CharField(max_length=255, choices=[
        ('connecting', 'Connecting'),
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('error', 'Error'),
    ], default='offline')
    bot_checkin = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # pragma: no cover
        return u'%s (%s)' % (self.team_name, self.team_id)

    def api_call(self, method, **kwargs):
        data = {
            'token': self.bot_access_token,
        }
        data.update(**kwargs)
        response = requests.post(
            'https://slack.com/api/%s' % (method,), data=data)
        return response.json()

    def get_users(self):
        response = self.api_call('users.list')
        return dict([(member['id'], member)
                     for member in response['members']])

    def get_absolute_url(self):
        return reverse('accounts:slack-detail', kwargs={
            'pk': self.pk,
        })

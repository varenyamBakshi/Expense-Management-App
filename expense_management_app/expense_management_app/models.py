from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Settlement(models.Model):
    group = models.ForeignKey('Group', related_name='group_settlements', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='receiver_settlements', on_delete=models.CASCADE)
    payer = models.ForeignKey('User', related_name='payer_settlements', on_delete=models.CASCADE)
    proof = models.FileField(null=True, upload_to=None, max_length=100)

    class Meta:
        verbose_name = 'Settlement'
        verbose_name_plural = 'Settlements'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('settlement_detail', kwargs={'id': self.id})


class Group(models.Model):
    users = models.ManyToManyField('User',related_name='groups')
    settlements = models.ForeignKey('Settlement', related_name='group', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'id': self.id})

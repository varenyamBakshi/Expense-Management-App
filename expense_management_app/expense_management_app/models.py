from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

#################### FURTHER SCOPE ####################
# Unique together constraints in models
#######################################################

class UserGroup(models.Model):
    users = models.ManyToManyField(User, related_name='user_groups')
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'pk': self.pk})

class Settlement(models.Model):
    group = models.ForeignKey(UserGroup, related_name='group_settlements', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_settlements', on_delete=models.CASCADE)
    payer = models.ForeignKey(User, related_name='payer_settlements', on_delete=models.CASCADE)
    proof = models.FileField(null=True, upload_to='proofs', max_length=100)

    class Meta:
        verbose_name = 'Settlement'
        verbose_name_plural = 'Settlements'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('settlement_detail', kwargs={'pk': self.pk})

class Expense(models.Model):
    name = models.CharField(max_length=100, default='hello')
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name='group_expenses')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    payer = models.ForeignKey(User, related_name='payer_expenses', on_delete=models.CASCADE)
    users_involved = models.ManyToManyField(User, related_name='all_expenses')

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("expense_detail", kwargs={'pk': self.pk})

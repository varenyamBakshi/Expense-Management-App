from django.contrib import admin
from .models import UserGroup, Settlement, Expense

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    pass

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass

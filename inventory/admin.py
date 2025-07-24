from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.hashers import make_password
from inventory.models import UserProfile,Products,Variant,SubVariant,ProductVariantMap,ProductVariantCombination,StockTransaction


class CustomUserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)
admin.site.register(Products)
admin.site.register(Variant)
admin.site.register(SubVariant)
admin.site.register(ProductVariantMap)
admin.site.register(ProductVariantCombination)
admin.site.register(StockTransaction)


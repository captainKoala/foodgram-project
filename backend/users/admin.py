from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    fields = ('username', 'last_name', 'first_name', 'email', 'password',
              'is_staff', 'groups')
    list_filter = ('username', 'email')
    search_fields = ('username', 'first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        """
        Если было изменение в поле пароль, сохраняет новый хешированный пароль.
        """
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()




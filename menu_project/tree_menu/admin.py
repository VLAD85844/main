from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('title', 'url', 'named_url', 'parent', 'order')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order', 'url', 'named_url')
    list_filter = ('menu', 'parent')
    search_fields = ('title', 'url')
    list_editable = ('order',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Исключаем возможность выбрать себя в качестве родителя
            form.base_fields['parent'].queryset = MenuItem.objects.exclude(pk=obj.pk)
        return form
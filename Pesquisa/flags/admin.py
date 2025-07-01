from django.contrib import admin
from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag_code', 'flag_emoji', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'flag_code')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'flag_emoji')
    ordering = ('name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'flag_code', 'is_active')
        }),
        ('Flag Preview', {
            'fields': ('flag_emoji',),
            'description': 'Preview of the flag emoji for this country'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def flag_emoji(self, obj):
        """Display flag emoji in admin list view."""
        return obj.flag_emoji
    flag_emoji.short_description = 'Flag'

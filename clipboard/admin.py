
from django.contrib import admin
from .models import Clipboard

@admin.register(Clipboard)
class ClipboardAdmin(admin.ModelAdmin):
    list_display = ('share_id', 'created_at')
    search_fields = ('text', 'share_id')
    list_filter = ('created_at',)

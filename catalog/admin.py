from django.contrib import admin

from catalog.models import LogModel


# Register your models here.

class LogModelAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = ["path", "method", "status", "has_query", "has_body", "timestamp"]
    list_filter = ["method", "status", "timestamp"]
    readonly_fields = ["timestamp"]
    fieldsets = [
        (None, {"fields": ["path", "method", "status"]}),
        ("Params", {"fields": ["query_get", "body_post"]}),
        ("Time stamp", {"fields": ["timestamp"]})
    ]


admin.site.register(LogModel, LogModelAdmin)

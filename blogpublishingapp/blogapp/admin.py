from django.contrib import admin

# Register your models here.
from .models import *
from chartjs.views.lines import BaseLineChartView
import pandas as pd
import plotly.express as px
from django.utils.html import format_html


class BlogmodelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_image', 'created_at', 'is_verified')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return 'No Image'

    display_image.allow_tags = True
    display_image.short_description = 'Image'

admin.site.register(Blogmodel, BlogmodelAdmin)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'password', 'display_profile_pic')

    def display_profile_pic(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="50" height="50">'.format(obj.profile_pic.url))
        else:
            return 'No Image'

    display_profile_pic.allow_tags = True
    display_profile_pic.short_description = 'Profile Picture'

admin.site.register(Registration, RegistrationAdmin)
class DraftsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'display_image')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50">'.format(obj.image.url))
        else:
            return 'No Image'
    display_image.allow_tags = True
    display_image.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        if not change:
            # Set the user field to the currently logged-in user
            obj.user = request.user
        super().save_model(request, obj, form, change)
admin.site.register(drafts, DraftsAdmin)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'rate')


class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ('blog', 'message')


admin.site.register(Rating, RatingAdmin)
admin.site.register(Feedbacks, FeedbacksAdmin)
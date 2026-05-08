from django.contrib import admin
from .models import Department, Semester, Subject, Resource, UserRegistrationData, PlatformReview, VideoLecture


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'file_type', 'uploaded_by')
    list_filter = ('file_type', 'subject__semester__department')
    search_fields = ('title', 'subject__name', 'uploaded_by__username')
    exclude = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        obj.save()


class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'created_at')
    list_filter = ('subject__semester__department',)
    search_fields = ('title', 'subject__name', 'uploaded_by__username')
    exclude = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        obj.save()


admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(UserRegistrationData)
admin.site.register(PlatformReview)
admin.site.register(VideoLecture, VideoLectureAdmin)
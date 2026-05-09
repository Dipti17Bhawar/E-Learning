from django.contrib import admin
from .models import Department, Semester, Subject, Resource, UserRegistrationData, PlatformReview, VideoLecture


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'file_type', 'uploaded_by', 'get_link')
    list_filter = ('file_type', 'subject__semester__department')
    search_fields = ('title', 'subject__name', 'uploaded_by__username')
    exclude = ('uploaded_by',)

    def get_fieldsets(self, request, obj=None):
        """Show different fields based on resource type"""
        fieldsets = (
            ('Basic Information', {
                'fields': ('subject', 'title', 'file_type')
            }),
        )
        
        # Check the current file_type to determine which content field to show
        if obj:
            file_type = obj.file_type
        else:
            file_type = request.GET.get('file_type', 'notes_pdf')
        
        if file_type == 'video':
            fieldsets += (
                ('Video Content - Choose One Option Below', {
                    'fields': ('video_url', 'file'),
                    'description': '⚠️ Choose either: (1) Paste a video URL (YouTube, Vimeo, etc.) OR (2) Upload a video file. You must provide at least one.'
                }),
            )
        else:
            fieldsets += (
                ('File Upload', {
                    'fields': ('file',),
                }),
            )
        
        return fieldsets

    def get_link(self, obj):
        """Display file or URL link in list view"""
        if obj.file_type == 'video':
            if obj.video_url:
                return f'<a href="{obj.video_url}" target="_blank">View URL</a>'
            elif obj.file:
                return f'<a href="{obj.file.url}" target="_blank">View File</a>'
            else:
                return 'No Link'
        else:
            return f'<a href="{obj.file.url}" target="_blank">Download</a>' if obj.file else 'N/A'
    get_link.short_description = 'Link'
    get_link.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        obj.save()


class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'created_at', 'video_url')
    list_filter = ('subject__semester__department', 'uploaded_by', 'created_at')
    search_fields = ('title', 'subject__name', 'uploaded_by__username', 'description')
    exclude = ('uploaded_by',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('subject', 'title', 'description')
        }),
        ('Video Content', {
            'fields': ('video_url',),
            'description': 'Provide a URL to the video (YouTube, Vimeo, etc.)'
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

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
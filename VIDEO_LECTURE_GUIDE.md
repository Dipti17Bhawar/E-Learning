# Video Lecture Management Guide

## Overview
The `VideoLecture` model now supports both **file uploads** and **external URLs** for hosting videos in the Learning Portal.

## VideoLecture Model

### Fields
- **subject** (ForeignKey): The subject this video belongs to
- **title** (CharField): Title of the video lecture
- **description** (TextField): Optional description
- **video_file** (FileField): Uploaded video file (MP4, WebM, OGG, MKV) - *Optional*
- **video_url** (URLField): External video URL (YouTube, Vimeo, etc.) - *Optional*
- **uploaded_by** (ForeignKey): The admin/user who uploaded it
- **created_at** (DateTimeField): Timestamp of creation

### Validation Rule
✅ **At least ONE of the following must be provided:**
- `video_file` - Local file upload
- `video_url` - External URL link

## Usage Methods

### Method 1: Admin Dashboard (Recommended)
1. Go to Django Admin: `/admin/`
2. Click on **Video Lectures**
3. Click **Add Video Lecture**
4. Fill in the form:
   - **Subject**: Select the subject
   - **Title**: Enter video title
   - **Description**: Add optional description
   - **Video File** (Option A): Upload an MP4, WebM, OGG, or MKV file
   - **Video URL** (Option B): Paste a YouTube, Vimeo, or other video platform URL
5. Click **Save**

**Note:** You only need to provide EITHER a file OR a URL, not both.

### Method 2: Management Command
For bulk uploads or scripting, use the custom command:

```bash
python manage.py add_video_lecture \
    --subject-id 1 \
    --title "Introduction to Django" \
    --url "https://www.youtube.com/watch?v=example" \
    --description "Basic Django concepts" \
    --uploaded-by-id 1
```

#### Command Arguments:
- `--subject-id` (required): ID of the subject
- `--title` (required): Title of the video
- `--url` (required): Video URL
- `--description` (optional): Video description
- `--uploaded-by-id` (optional): User ID of admin. If not provided, uses the first superuser.

#### Examples:

**Example 1: Add a YouTube video**
```bash
python manage.py add_video_lecture \
    --subject-id 5 \
    --title "Advanced Python Programming" \
    --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Example 2: Add with description**
```bash
python manage.py add_video_lecture \
    --subject-id 3 \
    --title "Web Development Basics" \
    --url "https://vimeo.com/123456789" \
    --description "Learn HTML, CSS, and JavaScript fundamentals"
```

**Example 3: Specify the uploading admin**
```bash
python manage.py add_video_lecture \
    --subject-id 2 \
    --title "Database Design" \
    --url "https://www.youtube.com/watch?v=abc123" \
    --uploaded-by-id 2
```

## File Upload Specifications

### Supported Formats:
- **MP4** (.mp4)
- **WebM** (.webm)
- **OGG** (.ogg)
- **Matroska** (.mkv)

### Upload Directory:
- Videos are stored in: `media/video_lectures/`

### File Size Recommendations:
- Keep files under 500MB for optimal performance
- Consider compressing videos before upload
- Use H.264 codec for MP4 files for best compatibility

## Frontend Display

When displaying videos in templates:
```django
{% for video in subject.video_lectures.all %}
    <div class="video-lecture">
        <h3>{{ video.title }}</h3>
        <p>{{ video.description }}</p>
        
        {% if video.video_file %}
            <!-- Embedded video player for uploaded files -->
            <video width="100%" controls>
                <source src="{{ video.video_file.url }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        {% elif video.video_url %}
            <!-- Embedded video for external URLs -->
            <iframe width="100%" height="400" src="{{ video.video_url }}" 
                    frameborder="0" allowfullscreen></iframe>
        {% endif %}
        
        <p class="meta">Uploaded by {{ video.uploaded_by.username }} on {{ video.created_at }}</p>
    </div>
{% endfor %}
```

## Admin Interface Features

The Django admin for VideoLecture now includes:
- ✅ **Dual-input support**: Upload files or paste URLs
- ✅ **Video source indicator**: Shows whether content is from file or URL
- ✅ **Direct links**: Quick access to view/download videos
- ✅ **Smart fieldsets**: Clear instructions for admins
- ✅ **Auto-uploaded_by**: Automatically records the uploading admin

## Database Schema

The migration `0017_videolecture_video_file_alter_videolecture_video_url.py` added:
- New `video_file` field (FileField)
- Modified `video_url` field to be optional (was required)

### SQL Changes:
```sql
ALTER TABLE TechSutraapp_videolecture ADD COLUMN video_file VARCHAR(100);
ALTER TABLE TechSutraapp_videolecture MODIFY COLUMN video_url VARCHAR(200) NULL;
```

## Troubleshooting

### Error: "Please provide either a video file or a video URL"
- **Cause**: Neither file nor URL was provided
- **Solution**: Upload a video file OR paste a valid URL

### Error: "File extension not allowed"
- **Cause**: Uploaded file format not supported
- **Solution**: Use only MP4, WebM, OGG, or MKV formats

### Error: "Invalid URL format"
- **Cause**: URL is malformed
- **Solution**: Ensure URL starts with `http://` or `https://`

### Video not displaying on frontend
- **Cause**: URL might not support embedding
- **Solution**: Test URL in browser first; some video platforms restrict embedding

## Best Practices

1. ✅ **Prefer URLs for external content**: YouTube, Vimeo videos use less server storage
2. ✅ **Use file uploads for proprietary content**: Important course materials should be stored locally
3. ✅ **Add descriptions**: Help students understand video content
4. ✅ **Use meaningful titles**: Makes videos easy to find
5. ✅ **Test before saving**: Verify URLs work before adding them
6. ✅ **Monitor storage**: Watch disk usage for file uploads

## API Example (for frontend developers)

```python
from TechSutraapp.models import VideoLecture, Subject

# Get all videos for a subject
subject = Subject.objects.get(id=1)
videos = subject.video_lectures.all()

# Get videos uploaded by a specific admin
admin_videos = VideoLecture.objects.filter(uploaded_by__id=2)

# Get recent videos
recent = VideoLecture.objects.order_by('-created_at')[:10]

# Filter by video source
url_videos = VideoLecture.objects.filter(video_url__isnull=False)
file_videos = VideoLecture.objects.filter(video_file__isnull=False)
```

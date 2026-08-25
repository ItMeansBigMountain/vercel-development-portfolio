# Render Free Django Admin + Media Pattern

Session-derived pattern for client-editable Django sites deployed on Render Free or any host plan without interactive shell access.

## Problem

After deploying a Django admin-backed site, the user could not run `python manage.py createsuperuser` because Render Free did not expose Shell. The client also uploaded an announcement image in admin, but it did not appear publicly in production.

## Superuser without Shell

Add a management command, e.g. `create_admin_from_env`, that reads:

- `ADMIN_USERNAME`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

Behavior:

1. If username/password are missing, print a warning and no-op so regular deploys do not fail.
2. `get_or_create(username=...)`.
3. Set `is_staff=True`, `is_superuser=True`, update email, and `set_password(password)`.
4. Save.

Run it from the host build command after migrations:

```bash
pip install -r requirements.txt && \
python manage.py collectstatic --noinput && \
python manage.py migrate && \
python manage.py create_admin_from_env
```

User workflow:

1. Add env vars in Render dashboard.
2. Manual Deploy latest commit.
3. Log into `/admin/`.
4. Remove `ADMIN_PASSWORD` from environment after login works; the user remains in the database.

## Uploaded Media in Production

With `DEBUG=False`, Django does not serve `MEDIA_URL` by default. For a fast prototype, you can add a URL route:

```python
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pta.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
```

This is acceptable as a short-term free-hosting workaround for low-traffic prototypes, but it is not the durable production answer.

Durable client-site media should use persistent storage:

- Cloudinary
- S3-compatible bucket
- Supabase Storage
- Render persistent disk on a paid plan

Warn the user that free ephemeral filesystem uploads may disappear on restart/redeploy.

### When the image tag shows only alt text / 404

If the public page renders an image tag like `/media/announcements/foo.png` but the URL returns `404`, the database still has the file name while the underlying Render Free filesystem file is gone. Adding a `MEDIA_URL` route is not enough after the file has disappeared.

Fast Render-Free workaround for small admin-uploaded images (announcements, flyers, newsletter cover images):

1. Add non-editable database fields beside each public-facing `ImageField`. Use a prefix matching the original field name so the pattern works for multiple models/fields:

```python
image = models.ImageField(upload_to='announcements/', blank=True)
image_data = models.BinaryField(blank=True, null=True, editable=False)
image_content_type = models.CharField(max_length=80, blank=True, editable=False)
image_filename = models.CharField(max_length=255, blank=True, editable=False)

cover_image = models.ImageField(upload_to='newsletters/covers/', blank=True)
cover_image_data = models.BinaryField(blank=True, null=True, editable=False)
cover_image_content_type = models.CharField(max_length=80, blank=True, editable=False)
cover_image_filename = models.CharField(max_length=255, blank=True, editable=False)
```

2. Override `save()` to read the uploaded image bytes before storage save, store them in the binary field, keep the content type, and seek back to position `0` so Django can still save the file normally:

```python
def save(self, *args, **kwargs):
    if self.cover_image:
        try:
            self.cover_image.open('rb')
            data = self.cover_image.read()
            if data:
                self.cover_image_data = data
                self.cover_image_content_type = (
                    getattr(self.cover_image.file, 'content_type', '')
                    or mimetypes.guess_type(self.cover_image.name)[0]
                    or 'image/png'
                )
                self.cover_image_filename = self.cover_image.name
            self.cover_image.seek(0)
        except Exception:
            # Keep any existing database-backed copy.
            pass
    super().save(*args, **kwargs)
```

3. Add an image source property that returns a `data:<type>;base64,...` URL only when bytes exist. Do **not** fall back to `self.image.url` / `self.cover_image.url` on Render Free if broken media tags are confusing users; hide the image until it is re-uploaded.

```python
@property
def cover_image_src(self):
    if self.cover_image_data:
        encoded = base64.b64encode(bytes(self.cover_image_data)).decode('ascii')
        return f'data:{self.cover_image_content_type or "image/png"};base64,{encoded}'
    return ''
```

4. Update every public template that renders customer/admin-uploaded images to use the DB-backed property:

```django
{% if newsletter.cover_image_src %}<img src="{{ newsletter.cover_image_src }}" alt="{{ newsletter.title }}">{% endif %}
{% if item.image_src %}<img src="{{ item.image_src }}" alt="{{ item.title }}">{% endif %}
```

5. Add tests that assert public pages contain `src="data:image/...;base64,` and do not contain `/media/newsletters/covers/` or `/media/announcements/` for uploaded images.

6. Tell the user that existing broken records must be re-uploaded once; the vanished file cannot be reconstructed from only the filename. Future uploads persist because the bytes are stored in the database.

This is a pragmatic prototype fix for small images, not ideal for large files. For durable production/client launch, move to Cloudinary/S3/Supabase/paid persistent disk.

## Admin UX Improvement

For volunteer/contact submissions, add an unreviewed count:

- override admin index template with a dashboard banner, or
- override `changelist_view()` to include a title like `Volunteer interest submissions — 3 unreviewed`, and
- provide an admin filter/action to mark selected submissions reviewed.

## Content Placement Lesson

For PTA/nonprofit sites, distinguish:

- Newsletter issues: archive page, newest-first.
- Announcements/flyers: homepage prominence while active (`publish_date <= today` and no expired `expires_date`).

This prevents urgent community updates from being hidden in a newsletter archive.

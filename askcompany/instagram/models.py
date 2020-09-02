from django.db import models

# Create your models here.
class Post(models.Model):
    message = models.TextField()
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%M/%D')
    is_public = models.BooleanField(default = False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
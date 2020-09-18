from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(
        validators=[MinLengthValidator(10)]
    )
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%M/%D')
    tag_set = models.ManyToManyField('tag', blank=True) # Tag 모델은 아래에 있기 때문에, 문자열로 명시
    is_public = models.BooleanField(default = False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])
    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 실제로 DB 필드에는 post_id 필드가 생성된다. (id는 Post의 PK)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    #post_set = models.ManyToManyField(Post)
    def __str__(self):
        return self.name
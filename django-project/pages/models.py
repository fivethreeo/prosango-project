from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='pages',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    images = models.ManyToManyField('filer.Image', blank=True, related_name='pages')

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

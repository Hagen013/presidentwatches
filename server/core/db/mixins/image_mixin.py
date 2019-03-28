from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToCover


class ImageMixin(models.Model):

    class Meta:
        abstract = True

    upload_image_to = None
    image_key_attribute = None

    thumbnail_width = 317
    thumbnail_height = 255
    thumbnail_upscale = True
    thumbnail_quality = 90

    image = models.ImageField(
        upload_to='images/',
        default='images/no_photo.png',
        blank=False,
        max_length=512
    )

    thumbnail = ImageSpecField(
        source='image',
        processors=[
            ResizeToCover(
                width=thumbnail_width,
                height=thumbnail_height,
                upscale=thumbnail_upscale,
            )
        ],
        options={'quality': thumbnail_quality}
    )

    @property
    def has_image(self):
        return self.image != self.image.field.default

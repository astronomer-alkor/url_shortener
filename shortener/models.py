from django.db import models


class Url(models.Model):
    process_id = models.IntegerField(null=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=20)

    @staticmethod
    def is_short_url_exist(short_url):
        return True if Url.objects.filter(short_url=short_url) else False

    @staticmethod
    def get_url_object(short_url):
        url = Url.objects.filter(short_url=short_url)
        if url:
            return url[0]
        return None

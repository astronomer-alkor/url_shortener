from .models import Url
from .base_62_converter import dehydrate


def generate_short_url(long_url, custom_url):
    if not custom_url:
        answer = Url.objects.filter(long_url=long_url)
        if answer:
            return answer[0].short_url
        new_row = Url.objects.create(long_url=long_url)
        new_row.save()
        new_row.process_id = new_row.id
        short_url = dehydrate(new_row.process_id)
        while Url.objects.filter(short_url=short_url):
            new_row.process_id += 1
            short_url = dehydrate(new_row.process_id)
        new_row.short_url = short_url
        new_row.save()
        return short_url
    new_row = Url.objects.create(long_url=long_url, short_url=custom_url)
    new_row.save()
    new_row.process_id = new_row.id
    new_row.save()
    return new_row.short_url

from django.utils.text import slugify


def create_unique_slug(title, model):
    base_slug = slugify(title)
    counter = 1
    while model.objects.filter(slug=base_slug).exists():
        base_slug = f'{base_slug}-{counter}'
        counter += 1
    return base_slug


from django.utils.text import slugify
import random, string


def generate_random_string(n):
    rs = ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
    return rs



def generate_slug(text):
    new_slug = slugify(text)

    from pp.models import Blog
    
    if Blog.objects.filter(slug = new_slug).first():
        return generate_slug(new_slug + generate_random_string(5))
    return new_slug
    

# def generate_slug(text):
#     new_slug = slugify(text)

        # from pp.models import Blog
    
#     if Blog.objects.filter(slug=new_slug).first():
#         return generate_slug(text + generate_random_string(5))
#     return new_slug

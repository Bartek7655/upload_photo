from uuid import uuid4


def uniq_path(instance, filename):
    extension, directory = filename.split('.')[-1], filename.split('.')[0]
    filename = f"{uuid4()}.{extension}"
    return f"{instance.user.pk}/images/{filename}"

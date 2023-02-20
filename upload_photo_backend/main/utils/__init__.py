
def uniq_path(instance, filename):
    extension, size = filename.split('.')[-1], filename.split('.')[-2]
    filename = f"{instance.user.username}_{size}.{extension}"
    return f"images/{instance.user.pk}/{filename}"

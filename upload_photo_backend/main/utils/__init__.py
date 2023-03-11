def uniq_path_original_image(instance, filename):
    name, extension = filename.split('.')[0], filename.split('.')[-1]

    return f"images/{instance.user.username}/{name}/{name}_original.{extension}"


def uniq_path_new_size_image(instance, filename):
    try:
        directory = filename.split('/')[2]
    except IndexError:
        directory = filename.split('.')[0].split("_")[0]

    filename = filename.split('/')[-1]

    return f"images/{instance.image.user.username}/{directory}/{filename}"

# Generated by Django 4.1.6 on 2023-02-23 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_sizeimage_binary_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typeaccount',
            old_name='binary_link',
            new_name='binary',
        ),
        migrations.AlterField(
            model_name='binaryimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='binary_link', to='main.image'),
        ),
    ]

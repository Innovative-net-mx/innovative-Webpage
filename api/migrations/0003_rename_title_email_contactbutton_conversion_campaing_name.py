# Generated by Django 4.1.3 on 2024-10-28 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_campaing_name_email_contactbutton_conversion_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email_contactbutton_conversion',
            old_name='title',
            new_name='campaing_name',
        ),
    ]

# Generated by Django 2.0.3 on 2018-03-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM_test', '0002_auto_20180328_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(to='CRM_test.Tag'),
        ),
        migrations.AlterField(
            model_name='role',
            name='menus',
            field=models.ManyToManyField(to='CRM_test.Menu'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(to='CRM_test.Role'),
        ),
    ]

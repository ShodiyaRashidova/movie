# Generated by Django 3.1.7 on 2021-03-20 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ('-created_date',), 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQ'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-created_date',), 'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
    ]
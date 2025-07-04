# Generated by Django 5.0.2 on 2025-05-30 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_financialcategory_expense_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizingCommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='organizing_committee/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]

# Generated by Django 5.1 on 2025-01-06 13:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DASHBOARD', '0007_remove_convention_activity_sector_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SettingConvention',
            new_name='Setting',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='settingconvention',
            new_name='setting',
        ),
        migrations.AlterField(
            model_name='convention',
            name='name',
            field=models.CharField(choices=[('C-SEC_COM', 'Convention du secteur commercial'), ('C-SEC_MIN', 'Convention du secteur minier'), ('C-SEC_PET', 'Convention du secteur pretrolier'), ('C-SEC_SAN', 'Convention du secteur sanitaire'), ('C-SEC_AGR', 'Convention du secteur agricole'), ('C-SEC_EDU', 'Convention du secteur éducatif'), ('C-SEC_TEC', 'Convention du secteur technologique'), ('C-SEC_TOU', 'Convention du secteur touristique'), ('C-IAS19', 'Convention selon la norme IAS 19'), ('C-SEC_AUT', "Convention d'un autre secteur d'activité")], max_length=150, unique=True),
        ),
    ]

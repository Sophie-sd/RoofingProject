from django.db import migrations, models


def seed_analytics_settings(apps, schema_editor):
    AnalyticsSettings = apps.get_model('core', 'AnalyticsSettings')
    AnalyticsSettings.objects.get_or_create(
        pk=1,
        defaults={
            'gtm_container_id': 'GTM-WCRM2Z4W',
            'google_ads_id': 'AW-18337015115',
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_estimate_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'gtm_container_id',
                    models.CharField(
                        blank=True,
                        default='GTM-WCRM2Z4W',
                        help_text='Наприклад GTM-XXXXXXX. Порожнє поле — тег вимкнено.',
                        max_length=32,
                        verbose_name='Google Tag Manager ID',
                    ),
                ),
                (
                    'google_ads_id',
                    models.CharField(
                        blank=True,
                        default='AW-18337015115',
                        help_text='Наприклад AW-XXXXXXXXXX. Порожнє поле — тег вимкнено.',
                        max_length=32,
                        verbose_name='Google Ads ID (gtag)',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Аналітика Google',
                'verbose_name_plural': 'Аналітика Google',
            },
        ),
        migrations.RunPython(seed_analytics_settings, migrations.RunPython.noop),
    ]

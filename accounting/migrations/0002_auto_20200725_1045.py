# Generated by Django 3.0.7 on 2020-07-25 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afm', models.CharField(max_length=9, unique=True, verbose_name='Κωδικός')),
                ('eponymia', models.CharField(max_length=70, unique=True, verbose_name='Επωνυμία')),
            ],
            options={
                'verbose_name': 'ΣΥΝΑΛΛΑΣΣΟΜΕΝΟΣ',
                'verbose_name_plural': 'ΣΥΝΑΛΛΑΣΣΟΜΕΝΟΙ',
            },
        ),
        migrations.AddField(
            model_name='tran',
            name='perigrafi',
            field=models.CharField(default='makal', max_length=70, verbose_name='Περιγραφή'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tran',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.Partner', verbose_name='Συναλλασσόμενος'),
        ),
    ]

# Generated by Django 2.1.11 on 2019-11-07 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20191106_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notecomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.NoteComment'),
        ),
    ]
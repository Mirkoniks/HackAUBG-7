from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('rocket_port_predictor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='missioninput',
            old_name='mission_name',
            new_name='rocket_name',
        ),
        migrations.RenameField(
            model_name='missioninput',
            old_name='budget_million',
            new_name='cost_million',
        ),
        migrations.AddField(
            model_name='missioninput',
            name='launch_status',
            field=models.CharField(default='success', max_length=20),
        ),
    ] 
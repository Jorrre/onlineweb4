# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("splash", "0002_splashyear_start_date")]

    operations = [
        migrations.AlterModelOptions(
            name="splashyear", options={"ordering": ("-start_date",)}
        )
    ]

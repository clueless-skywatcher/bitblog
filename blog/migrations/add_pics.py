from django.db import migrations, models

def add_welcome_card(apps, schema_editor):
    ProfileCard = apps.get_model("blog", "ProfileCard")
    welcome_card = ProfileCard(name = 'Welcome')
    welcome_card.save()

def add_welcome_sigil(apps, schema_editor):
    Sigil = apps.get_model("blog", "Sigil")
    welcome_sigil = Sigil(name='Radioactive')
    welcome_sigil.save()

def delete_all_cards(apps, schema_editor):
    ProfileCard = apps.get_model("blog", "ProfileCard")
    ProfileCard.objects.all().delete()

def delete_all_sigils(apps, schema_editor):
    Sigil = apps.get_model("blog", "Sigil")
    Sigil.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_welcome_card, delete_all_cards),
        migrations.RunPython(add_welcome_sigil, delete_all_sigils)
    ]
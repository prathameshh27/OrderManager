import os
from django.db import migrations
from dotenv import load_dotenv
from django.contrib.auth.models import User

load_dotenv()

def create_superuser(apps, schema_editor):
    username = os.environ.get('ADMIN_USERNAME', 'su')
    email = os.environ.get('ADMIN_EMAIL','')
    password = os.environ.get('ADMIN_PASSWORD','super.user.321')
    
    count = User.objects.filter(username=username).count()
    if count == 0:
        User.objects.create_superuser(username, email, password)

    
class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

import os

from django.db.models.signals import post_save, post_delete

from unboxftpd import models

def make_user_directory(sender, instance, created, **kwargs):
    if not os.path.exists(instance.home_directory):
        os.mkdir(instance.home_directory)

post_save.connect(make_user_directory, sender=models.FTPUser)

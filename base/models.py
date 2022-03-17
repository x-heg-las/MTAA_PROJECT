# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FileTypes(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_types'


class Files(models.Model):
    data = models.BinaryField(blank=True, null=True)
    file_type = models.ForeignKey('RequestTypes', models.DO_NOTHING)
    size = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class RequestTypes(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_types'


class Requests(models.Model):
    title = models.CharField(max_length=120)
    answered_by_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True, related_name='answered_by_request')
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='user_request')
    request_type = models.ForeignKey(RequestTypes, models.DO_NOTHING)
    file = models.ForeignKey(Files, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    call_requested = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requests'


class UserTypes(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_types'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=120)
    profile_img_file = models.ForeignKey(Files, models.DO_NOTHING, blank=True, null=True)
    user_type = models.ForeignKey(UserTypes, models.DO_NOTHING)
    password = models.CharField(max_length=64)
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

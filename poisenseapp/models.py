# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Hazardchemicals(models.Model):
    chemical_name = models.CharField(db_column='Chemical_Name', primary_key=True, max_length=255)  # Field name made lowercase.
    hazardstatementcode = models.CharField(db_column='HazardStatementCode', max_length=255)  # Field name made lowercase.
    hazard_statement = models.CharField(db_column='Hazard_Statement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hazard_word = models.CharField(db_column='Hazard_Word', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ghs_code = models.CharField(db_column='GHS_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HazardChemicals'
        unique_together = (('chemical_name', 'hazardstatementcode'),)


class Pictogramcode(models.Model):
    hazardstatementcode = models.CharField(db_column='HazardStatementCode', primary_key=True, max_length=255)  # Field name made lowercase.
    prevention_code = models.CharField(db_column='Prevention_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.
    response_code = models.CharField(db_column='Response_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.
    storage_code = models.CharField(db_column='Storage_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PictogramCode'


class Precautionstm(models.Model):
    pictogramcode = models.CharField(db_column='PictogramCode', primary_key=True, max_length=255)  # Field name made lowercase.
    statement = models.CharField(db_column='Statement', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrecautionStm'


class Altername(models.Model):
    category = models.CharField(primary_key=True, max_length=255)
    alternativeingredient = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'altername'
        unique_together = (('category', 'alternativeingredient'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Foodcontain(models.Model):
    allergycategory = models.CharField(primary_key=True, max_length=255)
    food_contains = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foodcontain'


class Signandtreatment(models.Model):
    categories = models.CharField(primary_key=True, max_length=255)
    symptoms = models.CharField(max_length=255)
    treatments = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'signandtreatment'

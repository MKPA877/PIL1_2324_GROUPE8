# Generated by Django 5.0.6 on 2024-06-19 17:20

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Masculin"), ("F", "Feminin")], max_length=1
                    ),
                ),
                ("date_of_birth", models.DateField(null=True)),
                ("place_of_birth", models.CharField(max_length=100)),
                ("bio", models.TextField(blank=True, null=True)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=128)),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/profile_pictures/"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CentresDInteret",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sport", models.BooleanField(default=False)),
                ("musique", models.BooleanField(default=False)),
                ("lecture", models.BooleanField(default=False)),
                ("voyage", models.BooleanField(default=False)),
                ("cinema", models.BooleanField(default=False)),
                ("technologie", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="centres_d_interet",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("accepted", models.BooleanField(default=False)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_connections",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_connections",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Friendship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("common_percentage", models.FloatField()),
                (
                    "user1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="messages/images/"
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True, null=True, upload_to="messages/videos/"
                    ),
                ),
                (
                    "document",
                    models.FileField(
                        blank=True, null=True, upload_to="messages/documents/"
                    ),
                ),
                (
                    "audio",
                    models.FileField(
                        blank=True, null=True, upload_to="messages/audio/"
                    ),
                ),
                ("date_envoi", models.DateTimeField(auto_now_add=True)),
                (
                    "connection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="app.connection",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="my_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrivateChat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "connection",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat",
                        to="app.connection",
                    ),
                ),
            ],
        ),
    ]

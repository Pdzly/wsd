# Generated by Django 5.1.3 on 2025-04-12 23:27

import uuid

import django.db.models.deletion
import django_lifecycle.mixins
import pgtrigger.compiler
import pgtrigger.migrations
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0010_remove_post_insert_insert_remove_post_update_update_and_more"),
        ("pghistory", "0006_delete_aggregateevent"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, verbose_name="Slug")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_index=True, verbose_name="Updated At"),
                ),
                (
                    "event",
                    models.CharField(
                        choices=[("LIKE", "Like"), ("COMMENT", "Comment")],
                        help_text="Event Type",
                        max_length=7,
                        verbose_name="Event",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Description of the notification. This is what the users will see.",
                        verbose_name="Description",
                    ),
                ),
                (
                    "is_read",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the notification has been read or not.",
                        verbose_name="Is read",
                    ),
                ),
                ("object_of_interest_object_id", models.UUIDField(db_index=True)),
                (
                    "object_of_interest_content_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "core"), ("model", "post")),
                            models.Q(("app_label", "core"), ("model", "postcomment")),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_object_of_interest+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User who received this notification.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="NotificationEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, db_index=False, null=True, verbose_name="Slug"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "event",
                    models.CharField(
                        choices=[("LIKE", "Like"), ("COMMENT", "Comment")],
                        help_text="Event Type",
                        max_length=7,
                        verbose_name="Event",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Description of the notification. This is what the users will see.",
                        verbose_name="Description",
                    ),
                ),
                (
                    "is_read",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the notification has been read or not.",
                        verbose_name="Is read",
                    ),
                ),
                ("object_of_interest_object_id", models.UUIDField()),
                (
                    "object_of_interest_content_type",
                    models.ForeignKey(
                        db_constraint=False,
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "core"), ("model", "post")),
                            models.Q(("app_label", "core"), ("model", "postcomment")),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "pgh_context",
                    models.ForeignKey(
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="pghistory.context",
                    ),
                ),
                (
                    "pgh_obj",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="events",
                        to="core.notification",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_constraint=False,
                        help_text="User who received this notification.",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="notification",
            trigger=pgtrigger.compiler.Trigger(
                name="insert_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "core_notificationevent" ("created_at", "description", "event", "id", "is_read", "object_of_interest_content_type_id", "object_of_interest_object_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "slug", "updated_at", "user_id") VALUES (NEW."created_at", NEW."description", NEW."event", NEW."id", NEW."is_read", NEW."object_of_interest_content_type_id", NEW."object_of_interest_object_id", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."slug", NEW."updated_at", NEW."user_id"); RETURN NULL;',
                    hash="f3d2284fab89ef35afb1f75bf79fa4762d9594e2",
                    operation="INSERT",
                    pgid="pgtrigger_insert_insert_4d81e",
                    table="core_notification",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="notification",
            trigger=pgtrigger.compiler.Trigger(
                name="update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "core_notificationevent" ("created_at", "description", "event", "id", "is_read", "object_of_interest_content_type_id", "object_of_interest_object_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "slug", "updated_at", "user_id") VALUES (NEW."created_at", NEW."description", NEW."event", NEW."id", NEW."is_read", NEW."object_of_interest_content_type_id", NEW."object_of_interest_object_id", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."slug", NEW."updated_at", NEW."user_id"); RETURN NULL;',
                    hash="561464346a982bd43cf9a4217d14fc4c9d732ac6",
                    operation="UPDATE",
                    pgid="pgtrigger_update_update_85197",
                    table="core_notification",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="notification",
            trigger=pgtrigger.compiler.Trigger(
                name="delete_delete",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "core_notificationevent" ("created_at", "description", "event", "id", "is_read", "object_of_interest_content_type_id", "object_of_interest_object_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "slug", "updated_at", "user_id") VALUES (OLD."created_at", OLD."description", OLD."event", OLD."id", OLD."is_read", OLD."object_of_interest_content_type_id", OLD."object_of_interest_object_id", _pgh_attach_context(), NOW(), \'delete\', OLD."id", OLD."slug", OLD."updated_at", OLD."user_id"); RETURN NULL;',
                    hash="497baf7cd0f7171e6852b087899b01e4c351055e",
                    operation="DELETE",
                    pgid="pgtrigger_delete_delete_1e0f6",
                    table="core_notification",
                    when="AFTER",
                ),
            ),
        ),
    ]

# Generated by Django 5.1.3 on 2025-04-06 18:34

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_postbookmark_post_bookmarked_users_postbookmarkevent_and_more"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="post",
            name="insert_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="post",
            name="update_update",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="post",
            name="delete_delete",
        ),
        migrations.AddField(
            model_name="post",
            name="is_nsfw",
            field=models.BooleanField(default=False, verbose_name="Is NSFW?"),
        ),
        migrations.AddField(
            model_name="postevent",
            name="is_nsfw",
            field=models.BooleanField(default=False, verbose_name="Is NSFW?"),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="post",
            trigger=pgtrigger.compiler.Trigger(
                name="insert_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "core_postevent" ("average_hash", "category_id", "colorhash", "created_at", "cryptographic_hash", "dhash", "extracted_text_normalized", "extracted_text_raw", "id", "image", "initial_id", "is_nsfw", "is_original", "is_repost", "original_source", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phash", "slug", "title", "updated_at", "user_id", "whash") VALUES (NEW."average_hash", NEW."category_id", NEW."colorhash", NEW."created_at", NEW."cryptographic_hash", NEW."dhash", NEW."extracted_text_normalized", NEW."extracted_text_raw", NEW."id", NEW."image", NEW."initial_id", NEW."is_nsfw", NEW."is_original", NEW."is_repost", NEW."original_source", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."phash", NEW."slug", NEW."title", NEW."updated_at", NEW."user_id", NEW."whash"); RETURN NULL;',
                    hash="72492c8a9166ceae1846f6cd6dc519d37018e2eb",
                    operation="INSERT",
                    pgid="pgtrigger_insert_insert_1a363",
                    table="core_post",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="post",
            trigger=pgtrigger.compiler.Trigger(
                name="update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "core_postevent" ("average_hash", "category_id", "colorhash", "created_at", "cryptographic_hash", "dhash", "extracted_text_normalized", "extracted_text_raw", "id", "image", "initial_id", "is_nsfw", "is_original", "is_repost", "original_source", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phash", "slug", "title", "updated_at", "user_id", "whash") VALUES (NEW."average_hash", NEW."category_id", NEW."colorhash", NEW."created_at", NEW."cryptographic_hash", NEW."dhash", NEW."extracted_text_normalized", NEW."extracted_text_raw", NEW."id", NEW."image", NEW."initial_id", NEW."is_nsfw", NEW."is_original", NEW."is_repost", NEW."original_source", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."phash", NEW."slug", NEW."title", NEW."updated_at", NEW."user_id", NEW."whash"); RETURN NULL;',
                    hash="98764965bf4a0a54d423063b0f23f4786086e96b",
                    operation="UPDATE",
                    pgid="pgtrigger_update_update_7429e",
                    table="core_post",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="post",
            trigger=pgtrigger.compiler.Trigger(
                name="delete_delete",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "core_postevent" ("average_hash", "category_id", "colorhash", "created_at", "cryptographic_hash", "dhash", "extracted_text_normalized", "extracted_text_raw", "id", "image", "initial_id", "is_nsfw", "is_original", "is_repost", "original_source", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phash", "slug", "title", "updated_at", "user_id", "whash") VALUES (OLD."average_hash", OLD."category_id", OLD."colorhash", OLD."created_at", OLD."cryptographic_hash", OLD."dhash", OLD."extracted_text_normalized", OLD."extracted_text_raw", OLD."id", OLD."image", OLD."initial_id", OLD."is_nsfw", OLD."is_original", OLD."is_repost", OLD."original_source", _pgh_attach_context(), NOW(), \'delete\', OLD."id", OLD."phash", OLD."slug", OLD."title", OLD."updated_at", OLD."user_id", OLD."whash"); RETURN NULL;',
                    hash="ecc62c49a170d4645827797e6624b858f025fa42",
                    operation="DELETE",
                    pgid="pgtrigger_delete_delete_edf98",
                    table="core_post",
                    when="AFTER",
                ),
            ),
        ),
    ]

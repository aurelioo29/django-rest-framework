# Generated by Django 5.0.6 on 2024-05-08 12:19

import django.db.models.deletion
import pos_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pos_app", "0004_alter_tableresto_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="status_category",
                        to="pos_app.statusmodel",
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_create_category",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_update_category",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuResto",
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
                    "code",
                    models.CharField(
                        default=pos_app.models.increment_menu_resto_code,
                        editable=False,
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("decription", models.CharField(max_length=200)),
                (
                    "image_menu",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="menu_images/"
                    ),
                ),
                (
                    "menu_status",
                    models.CharField(
                        choices=[("Ada", "Ada"), ("Habis", "Habis")],
                        default="Ada",
                        max_length=15,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_menu",
                        to="pos_app.category",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="status_menu",
                        to="pos_app.statusmodel",
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_create_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_update_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderMenu",
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
                    "code",
                    models.CharField(
                        default=pos_app.models.increment_order_menu_code,
                        editable=False,
                        max_length=20,
                    ),
                ),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("Belum Dibayar", "Belum Dibayar"),
                            ("Sudah Dibayar", "Sudah Dibayar"),
                            ("Selesai", "Selesai"),
                        ],
                        default="Belum Dibayar",
                        max_length=15,
                    ),
                ),
                (
                    "total_order",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("tax_order", models.FloatField(blank=True, default=0, null=True)),
                (
                    "total_payment",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "payment",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "changed",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "cashier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="cashier_order_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="status_order_menu",
                        to="pos_app.statusmodel",
                    ),
                ),
                (
                    "table_resto",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="table_resto_order_menu",
                        to="pos_app.tableresto",
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_create_order_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_update_order_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "waitress",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="waitress_order_menu",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderMenuDetail",
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
                ("quantity", models.IntegerField(default=0)),
                (
                    "subtotal",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=200, null=True),
                ),
                (
                    "order_menu_detail_status",
                    models.CharField(
                        choices=[
                            ("Sedang disiapkan", "Sedang disiapkan"),
                            ("Sudah disajikan", "Sudah disajikan"),
                        ],
                        default="Sedang disiapkan",
                        max_length=20,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "menu_resto",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="menu_resto_order_menu_detail",
                        to="pos_app.menuresto",
                    ),
                ),
                (
                    "order_menu",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order_menu_order_menu_detail",
                        to="pos_app.ordermenu",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="status_order_menu_detail",
                        to="pos_app.statusmodel",
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_create_order_menu_detail",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_update_order_menu_detail",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                    "avatar",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="profile_images/"
                    ),
                ),
                ("bio", models.TextField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="status_profile",
                        to="pos_app.statusmodel",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_create",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_create_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_update",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_update_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

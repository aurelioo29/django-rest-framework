from django.contrib import admin
from pos_app.models import User, TableResto, StatusModel, Category, MenuResto, OrderMenu, OrderMenuDetail, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(TableResto)
admin.site.register(StatusModel)
admin.site.register(Category)
admin.site.register(MenuResto)
admin.site.register(OrderMenu)
admin.site.register(OrderMenuDetail)
admin.site.register(Profile)

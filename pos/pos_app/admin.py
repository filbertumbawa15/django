from django.contrib import admin
from pos_app.models import (
        User, TableResto, Category
    )

admin.site.register(User)
admin.site.register(TableResto)
admin.site.register(Category)

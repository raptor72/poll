from django.contrib import admin

import nested_admin

from .models import Poll, Question, Choice, Vote, User


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 1


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    sortable_field_name = "order"
    inlines = [ChoiceInline]


class TableofChoiceAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


class VoteInline(admin.TabularInline):
    model = Vote


class UserAdmin(admin.ModelAdmin):
    inlines = [VoteInline]


admin.site.register(Poll, TableofChoiceAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


from django.contrib import admin

import nested_admin

from .models import Poll, Question, Choice, Vote


#admin.site.register(Poll)
#admin.site.register(Question)
#admin.site.register(Choice)
#admin.site.register(Vote)

class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 1

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    sortable_field_name = "order"
    inlines = [ChoiceInline,]


class TableofChoiceAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Poll, TableofChoiceAdmin)

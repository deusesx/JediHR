# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Planet, Jedi, Test, Question, Answer

admin.site.register(Planet)
admin.site.register(Jedi)
admin.site.register(Question)

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3
    exclude = ('answer',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    model = Test
    inlines = [AnswerInline, ]

from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    
    
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    search_fields = ['question_text']
    date_hierarchy = 'pub_date'
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    
admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    raw_id_fields = ['question']
admin.site.register(Choice, ChoiceAdmin)

from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]

class ChoiceAdmin(admin.ModelAdmin):
    fields = ["votes", "choice_text", "question"]
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
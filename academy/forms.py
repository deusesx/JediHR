# -*- coding: utf-8 -*-
from django import forms
from .models import Candidate, Test, Answer, Jedi


class CandidateForm(forms.ModelForm):

    class Meta(object):
        model = Candidate
        exclude = ('is_padavan', 'test_done', 'teacher')


class AnswerForm(forms.ModelForm):

    class Meta(object):
        model = Answer
        fields = ('answer', )


AnswersFormset = forms.modelformset_factory(Answer, form=AnswerForm, fields=['answer'], extra=0)
AnswersInlineFormset = forms.inlineformset_factory(Test, Answer, formset=AnswersFormset, extra=0, can_delete=False, fields=['answer'])


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        exclude = ('test_result', 'questions', 'candidate', 'answers')


class JediChooseForm(forms.Form):
    jedi_choose = forms.ModelChoiceField(queryset=Jedi.objects.all(), empty_label='Выберите себя из списка',
                                         label='Войти как')


class MakePadavanForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['teacher']

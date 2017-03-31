from django.shortcuts import reverse, redirect, render
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.mail import EmailMessage

from .models import Candidate, Test, Answer, Jedi, Planet, Question
from .forms import CandidateForm, TestForm,  AnswersInlineFormset, JediChooseForm, MakePadavanForm


def main_view(request):
    return render(request, template_name='academy/main_view.html')


# эпик кандидата
class CandidateCreate(CreateView):
    form_class = CandidateForm
    model = Candidate

    def get_success_url(self):
        return reverse('candidate_success', args=(self.object.id, ))


class TestUpdate(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'academy/test_form.html'

    def get_success_url(self):
        return reverse('test_passed', args=(self.object.test_unique_code, ))


def candidate_test_answers(request, test_uc):
    if request.method == 'POST':
        formset = AnswersInlineFormset(request.POST or None)
        if formset.is_valid():
            formset.save()
            candidate = Test.objects.get(test_unique_code=test_uc).candidate
            candidate.test_done = True
            candidate.save()
            return redirect(reverse('test_passed', args=(test_uc,)))
    else:
        test = Test.objects.get(test_unique_code=test_uc)
        answers = AnswersInlineFormset(queryset= Answer.objects.filter(test=test))
        return render(request, context=locals(), template_name='academy/test_form.html')


def candidate_success_view(request, pk):
    candidate = Candidate.objects.get(id = pk)
    test = Test.objects.filter(candidate = candidate)
    if test.count() == 1:
        return redirect(reverse('test_update', args=(test[0].test_unique_code, )))
    else:
        return render(request, context=locals(), template_name='academy/candidate_success.html')


def test_passed_view(request, pk):
    test = Test.objects.get(test_unique_code=pk)
    return render(request, context={'test': pk, 'candidate': test.candidate}, template_name='academy/test_passed.html')


# эпик джедая
class JediChooseView(FormView):
    form_class = JediChooseForm
    template_name = 'academy/jedi_choose.html'
    success_url = '/jedi/choose/'

    def form_valid(self, form):
        jedi = Jedi.objects.get(pk=form.data['jedi_choose'])
        planet = jedi.planet_id
        self.success_url = '/planet/' + str(planet) + '/candidates/?passed=True&is_padavan=False'
        return super(JediChooseView, self).form_valid(form)


class CandidateList(ListView):
    model = Candidate
    template_name = 'academy/jedi_choose_padavans.html'

    def get_queryset(self):
        queryset = Candidate.objects.all()

        if self.request.method == 'GET':
            test_done = self.request.GET.get('passed')
            is_padavan = self.request.GET.get('is_padavan')
            if test_done is not None:
                queryset = queryset.filter(test_done=test_done)
            if is_padavan is not None:
                queryset = queryset.filter(is_padavan=is_padavan)

            if self.kwargs.get('planet_pk') is not None:
                planet = Planet.objects.get(pk=self.kwargs.get('planet_pk'))
                queryset = queryset.filter(planet=planet)

        return queryset


class CandidateDetailView(DetailView, FormMixin):
    model = Candidate
    form_class = MakePadavanForm
    template_name = 'academy/candidate_answers.html'
    context_object_name = 'candidate'

    def get_success_url(self):
        return reverse(self.request.resolver_match.view_name, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(CandidateDetailView, self).get_context_data(**kwargs)
        context['test'] = Test.objects.get(candidate=self.kwargs.get('pk'))
        context['answers'] = Answer.objects.filter(test=context['test'])
        context['questions'] = Question.objects.filter(test=context['test'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        candidate = self.object
        if form.data['teacher'] != '':
            candidate.teacher = Jedi.objects.get(id=form.data['teacher'])
            candidate.is_padavan = True
            candidate.save()
            message = ' '.join(['Поздравляем,', str(candidate.name), '!\n Вы зачислены в падаваны к джедаю',
                                candidate.teacher.name])
            email = EmailMessage('Вы зачислены в падаваны', message, 'samigullin.art@gmail.com', [str(candidate.email)])
            email.send()
        return super(CandidateDetailView, self).form_valid(form)

    def get_initial(self):
        initial = super(CandidateDetailView, self).get_initial()
        initial['teacher'] = Candidate.objects.get(id=self.kwargs.get('pk')).teacher
        return initial

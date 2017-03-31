# -*- coding: utf-8 -*-
from django.db import models


class Planet(models.Model):
    """
    Сущность Планета
    """
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Jedi(models.Model):
    """
    Сущность Джедай
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    planet = models.OneToOneField(Planet)

    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    """
    Сущность Вопрос
    """
    text = models.TextField(verbose_name='Текст вопроса')
    right_answer = models.BooleanField(verbose_name='Правильный ответ',
                                       help_text='Поставьте галочку если правильный ответ "да". Оставьте пустым если правильный ответ "нет"')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def check_question(self, answer):
        return answer == self.right_answer

    def __unicode__(self):
        return str("Вопрос " + str(self.id))

    def __str__(self):
        return str("Вопрос " + str(self.id))


class Candidate(models.Model):
    """
    Сущность Кандидат
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    planet = models.ForeignKey(Planet, verbose_name='Планета обитания')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    email = models.EmailField(verbose_name='Электронная почта')
    is_padavan = models.BooleanField(default=False)
    test_done = models.BooleanField(default=False)
    teacher = models.ForeignKey(Jedi, null=True, blank=True, verbose_name='Учитель')

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Test(models.Model):
    """
    Сущность Тестовое Испытание Кандидата
    """
    test_unique_code = models.AutoField(primary_key=True, verbose_name='Уникальный код ордена')
    candidate = models.OneToOneField(Candidate, verbose_name='Кандидат')
    from_jedi = models.ForeignKey(Jedi, verbose_name="Назначено джедаем")
    test_result = models.NullBooleanField(verbose_name='Результат', blank=True, default=None)
    questions = models.ManyToManyField(Question, through='Answer')

    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'

    def __unicode__(self):
        return str(self.candidate.name + "_" + str(self.test_unique_code))

    def __str__(self):
        return str(self.candidate.name + "_" + str(self.test_unique_code))


class Answer(models.Model):
    """
    Сущность Ответ
    Промежуточная сущность отношения Многие-ко-Многим между сущностью Вопрос и
    сущностью Тестовое Испытание Кандидата
    """
    question = models.ForeignKey(Question, verbose_name='Вопрос')
    test = models.ForeignKey(Test)
    answer = models.NullBooleanField(default=None, verbose_name='Ответ')

    class Meta:
        verbose_name = "Вопрос кандидату"
        verbose_name_plural = "Вопросы кандидату"

    def __unicode__(self):
        return str("Вопрос " + str(self.question_id))

    def __str__(self):
        return str("Вопрос " + str(self.question_id))

    def get_question_text(self):
        return self.question.text
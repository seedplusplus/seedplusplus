from django.test import TestCase

from lesson.models import Lesson,Curriculum

class LessonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Lesson.objects.create(title='TestLesson', language='English')

    def test_title_label(self):
        lesson = Lesson.objects.get(id=1)
        field_label = lesson._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')


    def test_title_max_length(self):
        lesson = Lesson.objects.get(id=1)
        max_length = lesson._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_language_label(self):
        lesson = Lesson.objects.get(id=1)
        field_label = lesson._meta.get_field('language').verbose_name
        self.assertEquals(field_label, 'language')


    def test_language_max_length(self):
        lesson = Lesson.objects.get(id=1)
        max_length = lesson._meta.get_field('language').max_length
        self.assertEquals(max_length, 30)

class CurriculumModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Lesson.objects.create(title='TestLesson1', language='English')
        Lesson.objects.create(title='TestLesson2', language='Spanish')
        Curriculum.objects.create(title='TestCurriculum')
        Curriculum.objects.get(id=1).lessons.set([Lesson.objects.get(id=1),Lesson.objects.get(id=2)])

    def test_title_label(self):
        curric = Curriculum.objects.get(id=1)
        field_label = curric._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')


    def test_title_max_length(self):
        curric = Curriculum.objects.get(id=1)
        max_length = curric._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_added_lessons(self):
    	curric = Curriculum.objects.get(id=1)
    	num_lessons = len(curric.lessons.all())
    	self.assertEquals(num_lessons,2)


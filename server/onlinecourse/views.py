from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Course, Enrollment, Learner, Question, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/index.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        {'course': course},
    )


def extract_answers(request):
    selected_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_ids.append(value)
    return Choice.objects.filter(id__in=selected_ids)


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    learner, _learner_created = Learner.objects.get_or_create(user=request.user)
    enrollment, _created = Enrollment.objects.get_or_create(
        learner=learner,
        course=course,
    )
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            args=(course_id, submission.id),
        )
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    choices = submission.choices.all()
    selected_ids = set(choices.values_list('id', flat=True))
    total_score = 0
    total_grade = 0

    for question in Question.objects.filter(course=course):
        total_grade += question.grade
        correct_ids = set(
            question.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        question_selected_ids = set(
            question.choice_set.filter(id__in=selected_ids).values_list('id', flat=True)
        )
        if correct_ids == question_selected_ids:
            total_score += question.grade

    passed = total_grade == 0 or total_score >= total_grade * 0.8
    context = {
        'course': course,
        'choices': choices,
        'grade': total_score,
        'passed': passed,
        'total_grade': total_grade,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

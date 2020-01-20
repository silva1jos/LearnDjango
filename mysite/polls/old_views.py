from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list, }
    return render(request, 'polls/index.html', context)

# Detail and results are the same


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    # alt: question = django.shortcuts.get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request,
                      'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select a choice.", })
    # They include an else: here i think thats not needed as return in except
    selected_choice.votes += 1
    selected_choice.save()
    # Do a HttpResponseRedirect afer successful post, stops user from posting 2x if they hit back
    return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))

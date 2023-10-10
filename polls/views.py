
import time 
from django.shortcuts import render, loader, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def clear_session(request, question_id):
    try:
        del request.session['has_voted_' + str(question_id)]
    except KeyError:
        return HttpResponse("You have not voted yet.")
    return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        if 'has_voted_' + str(question.id) in request.session:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You have already voted for this question.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            request.session['has_voted_' + str(question.id)] = True
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
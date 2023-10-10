
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

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Get the user's previous vote, if any
    previous_choice_id = request.session.get('has_voted_' + str(question.id))

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

    if previous_choice_id:
        # User has already voted, update their vote
        previous_choice = get_object_or_404(Choice, pk=previous_choice_id)
        previous_choice.votes -= 1
        previous_choice.save()
    
    selected_choice.votes += 1
    selected_choice.save()
    
    # Update the user's session to store the new choice they voted for
    request.session['has_voted_' + str(question.id)] = selected_choice.id
    
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

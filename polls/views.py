from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView): #()인자안에 부모 클래스가 들어감
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """Return the last five published questions."""
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

# def index(request):
#     #return HttpResponse("한재원(2005991) Hello world!")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     #template = loader.get_template('polls/index.html')
#     context = {'latest_question_list':latest_question_list,}
#     return render(request, 'polls/index.html', context)
#
# def detail(request,question_id):
#     #return HttpResponse("You're looking at question %s." % question_id)
#     # try:
#     #   question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #    raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})
#
# def results(request,question_id):
#     question= get_object_or_404(Question, pk=question_id)
#     #response = HttpResponse("You're looking at the results of question %s." % question_id)
#     return render(request, 'polls/results.html',{'question':question})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

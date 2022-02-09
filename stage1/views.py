from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Item, Reviewer, ReviewSentence, Aspect, Answer, Review, UserItem
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Top page of stage1")


@login_required
def item_board(request):
    user_items = UserItem.objects.all().filter(author=request.user)
    context = {'useritems': user_items}
    return render(request, 'stage1/item_board.html', context)


@login_required
def item_detail(request, item_id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(id=item_id)
            user_item = UserItem.objects.get(author=request.user, item=item)
        except (KeyError, Item.DoesNotExist, UserItem.DoesNotExist):
            user_items = UserItem.objects.all().filter(author=request.user)
            context = {'useritems': user_items, 'error_message': 'No such item to judge.'}
            return render(request, 'stage1/item_board.html', context)

        if user_item.done:
            user_items = UserItem.objects.all().filter(author=request.user)
            context = {'useritems': user_items,
                       'error_message': 'This item is already judged, please go to check the next unjudged one.'}
            return render(request, 'stage1/item_board.html', context)

        reviews = Review.objects.all().filter(item=item)
        sentences = ReviewSentence.objects.none()
        for review in reviews:
            s = ReviewSentence.objects.all().filter(review=review)
            sentences = sentences | s
        context = {'item': item, 'sentences': sentences}
        return render(request, 'stage1/item_detail.html', context)

    elif request.method == 'POST':
        item = Item.objects.get(id=item_id)
        author = request.user
        sentences = request.POST.getlist('sentence')

        if len(sentences) == 0:
            reviews = Review.objects.all().filter(item=item)
            review_sentences = ReviewSentence.objects.none()
            for review in reviews:
                s = ReviewSentence.objects.all().filter(review=review)
                review_sentences = review_sentences | s
            context = {'item': item, 'sentences': review_sentences, 'error_message': "You haven't choose any sentence."}
            return render(request, 'stage1/item_detail.html', context)

        user_item = UserItem.objects.get(author=author, item=item)
        user_item.done = True
        user_item.save()
        for s in sentences:
            sentence = ReviewSentence.objects.get(id=s)
            new_answer = Answer(author=author, item=item, sentence=sentence)
            new_answer.save()

        return redirect(reverse(item_board))


def group_board(request):
    return None
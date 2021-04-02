from django.shortcuts import render, redirect
from .forms import MessageForm, CommentForm
from .models import Message, Comment
from ..login.models import User
from django.template.defaulttags import register


def show_messages(request):

    if "user_id" not in request.session:
        return redirect('/')

    message_form = MessageForm()
    posted_messages = Message.objects.all().order_by('-created_at')
    comment_forms = create_comment_forms(posted_messages)
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)

    context = {
        'message_form': message_form,
        'comment_forms': comment_forms,
        'posted_messages': posted_messages,
        "user": User.objects.get(id=user_id)
    }

    return render(request, "messages.html", context)


def new_message(request):

    if request.method == "GET":
        return redirect('/wall/')

    if request.method == "POST":
        user_id = request.session["user_id"]
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            posted_message = message_form.save(commit=False)
            user_posting = User.objects.get(id=user_id)
            posted_message.user = user_posting
            posted_message.save()
            return redirect('/wall')

        posted_messages = Message.objects.all().order_by('-created_at')
        comment_forms = create_comment_forms(posted_messages)
        context = {
            "message_form": message_form,
            "comment_forms": comment_forms,
            'posted_messages': posted_messages,
            "user": User.objects.get(id=user_id)
        }
        return render(request, "messages.html", context)


def new_comment(request):

    if request.method == "GET":
        return redirect('/wall/')

    if request.method == "POST":
        message_commented_id = request.POST["message_commented_id"]
        user_id = request.session["user_id"]
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            posted_comment = comment_form.save(commit=False)
            message_commented = Message.objects.get(id=message_commented_id)
            posted_comment.message = message_commented
            user_posting = User.objects.get(id=user_id)
            posted_comment.user = user_posting
            posted_comment.save()
            return redirect('/wall')

        posted_messages = Message.objects.all()
        comment_forms = create_comment_forms(posted_messages)
        comment_forms[int(message_commented_id)] = comment_form
        message_form = MessageForm()
        context = {
            "message_form": message_form,
            "comment_forms": comment_forms,
            'posted_messages': posted_messages,
            "user": User.objects.get(id=user_id)
        }
        return render(request, "messages.html", context)


def create_comment_forms(messages):
    comment_forms = {}
    for message in messages:
        comment_forms[message.id] = CommentForm(
            initial={"message_commented_id": message.id}
    )
    return comment_forms


@register.filter
def get_item(dictionary, key):
        return dictionary.get(key)

from django.shortcuts import render
from django.http import HttpResponse
from .models import Text


def see_all_texts(request):
    texts = Text.objects.all()
    return render(
        request,
        "all_texts.html",
        {
            "texts": texts,
            "title": "titles from django",
        },
    )


def see_one_text(request, text_pk):
    try:
        text = Text.objects.get(pk=text_pk)
        return render(
            request,
            "text_detail.html",
            {
                "text": text,
            },
        )
    except Text.DoesNotExist:
        return render(
            request,
            "text_detail.html",
            {
                "not_found": True,
            },
        )

import datetime
from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .baseconv import base62
from .models import Link, Click
from .forms import LinkSubmitForm


@require_GET
def follow(request, base62_id):
    """
    View which gets the link for the given base62_id value
    and redirects to it.
    """
    link = get_object_or_404(Link, id=base62.to_decimal(base62_id))
    link.usage_count = F('usage_count') + 1
    link.save()
    click = Click(link = link).save()

    return HttpResponsePermanentRedirect(link.url)


@require_GET
def info(request, base62_id):
    """
    View which shows information on a particular link
    """
    link = get_object_or_404(Link, id=base62.to_decimal(base62_id))
    clicks = Click.objects.filter(link=link).order_by('-datetime')
    return render(request, 'shortener/link_info.html', {'link': link, 'clicks': clicks})


@require_POST
def submit(request):
    """
    View for submitting a URL to be shortened
    """
    form = LinkSubmitForm(request.POST)
    if form.is_valid():
        kwargs = {'url': form.cleaned_data['url']}

        if request.user.is_authenticated():
            kwargs.update({'user': request.user})
            print "user -----------"
            print request.user
        custom = form.cleaned_data['custom']
        if custom:
            # specify an explicit id corresponding to the custom url
            kwargs.update({'id': base62.to_decimal(custom)})
        link = Link.objects.create(**kwargs)
        return render(request, 'shortener/submit_success.html', {'link': link})
    else:
        return render(request, 'shortener/submit_failed.html', {'link_form': form})


@require_GET
def index(request):
    """
    View for main page
    """
    user_value = request.user if request.user.is_authenticated() else None

    values = {
        'link_form': LinkSubmitForm(),
        'recent_links': Link.objects.filter(user=user_value).order_by('-date_submitted')[:5],
        'most_popular_links': Link.objects.filter(user=user_value).order_by('-usage_count')[:5]}

    if user_value:
        values.update({'your_links':  Link.objects.filter(user=user_value).order_by('-date_submitted')})
    return render(request, 'shortener/index.html', values)

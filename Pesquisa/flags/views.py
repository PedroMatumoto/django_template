from django.shortcuts import render
from django.http import JsonResponse
from .models import Country


def examples(request):
    """Display flag system examples."""
    return render(request, 'flags/examples.html')


def countries_api(request):
    """API endpoint to get countries data."""
    countries = Country.objects.filter(is_active=True).values('code', 'name', 'flag_code')
    return JsonResponse(list(countries), safe=False)


def country_detail(request, country_code):
    """Display details for a specific country."""
    try:
        country = Country.objects.get(code=country_code.upper(), is_active=True)
        context = {
            'country': country,
        }
        return render(request, 'flags/country_detail.html', context)
    except Country.DoesNotExist:
        return render(request, 'flags/country_not_found.html', {'country_code': country_code})

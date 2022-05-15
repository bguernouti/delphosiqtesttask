from typing import Dict, Any, List
from django.db import models # Will be used for typing hints only

import requests
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from loans.serializers import CountrySerializer, LoanTitleSerializer, LoanSerializer, SectorSerializer
from loans.models import Country, Sector, Loan


def get_or_create(model: models.Model, filter_kwrgs: Dict, create_kwrgs: Dict) -> models.Model:
    if model.objects.filter(**filter_kwrgs).exists():
        # Check if the record exists and return it
        obj: models.Model = model.objects.get(**filter_kwrgs)
    else:
        # Create a new record
        obj: models.Model = model.objects.create(**create_kwrgs)
        obj.save()
    return obj


@csrf_exempt
def scrape_data(rq):
    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    """
    With a small work with the developer tools i found this url that return the data in a JSON format
    """
    url = "https://www.eib.org/provider-eib-plr/app/loans/list" \
               "?search=&sortColumn=loanParts.loanPartStatus.statusDate&sortDir=desc&" \
               "pageNumber=0&itemPerPage=100&pageable=true&language=EN&defaultLanguage=EN&" \
               "loanPartYearFrom=1959&loanPartYearTo=2022&orCountries.region=true&orCountries=true&orSectors=true"

    r = requests.get(url)
    data = r.json()

    projects = data['data']

    for project in projects:
        _signature_date = date.fromtimestamp(project['additionalInformation'][1]/1000)
        _signed_amount = project['additionalInformation'][0]
        _title = project['title']
        _country = project['primaryTags'][0]['label']
        _sector = project['primaryTags'][2]['label']

        country: Country = get_or_create(Country, {'name': _country}, {'name': _country})
        sector: Sector = get_or_create(Sector, {'name': _sector}, {'name': _sector})

        loan: Loan = Loan(
            signature_date=_signature_date,
            title=_title,
            country=country,
            sector=sector,
            signed_amount=_signed_amount
        )
        loan.save()

    return JsonResponse({'detail': 'data created!'}, status=status.HTTP_200_OK)


@csrf_exempt
def clear_data(rq):

    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    Loan.objects.all().delete()
    Country.objects.all().delete()
    Sector.objects.all().delete()
    return JsonResponse({'detail': 'data deleted!'}, status=status.HTTP_200_OK)


@csrf_exempt
def get_countries(rq):
    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    countries: List[Country] = Country.objects.all()
    serialized: CountrySerializer = CountrySerializer(countries, many=True)
    return JsonResponse(serialized.data, safe=False)


@csrf_exempt
def get_sectors(rq):
    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    sectors: List[Sector] = Sector.objects.all()
    serialized: SectorSerializer = SectorSerializer(sectors, many=True)
    return JsonResponse(serialized.data, safe=False)


@csrf_exempt
def get_projects(rq):
    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    projects: List[Loan] = Loan.objects.all()
    serialized: LoanTitleSerializer = LoanTitleSerializer(projects, many=True)
    return JsonResponse(serialized.data, safe=False)


@csrf_exempt
def get_loans(rq):
    if rq.method != 'GET':
        return JsonResponse({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    loans: List[Loan] = Loan.objects.all()
    serialized: LoanSerializer = LoanSerializer(loans, many=True)
    return JsonResponse(serialized.data, safe=False, json_dumps_params={'ensure_ascii': False})


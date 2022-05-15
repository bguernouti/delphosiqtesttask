from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)


class Sector(models.Model):
    name = models.CharField(max_length=100)


class Loan(models.Model):
    signature_date = models.DateField(auto_now=False, auto_now_add=False)
    title = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    signed_amount = models.CharField(max_length=100)

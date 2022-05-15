from rest_framework import serializers
from loans.models import Country, Sector, Loan


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']


class LoanTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'title']


class LoanSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    sector = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Loan
        fields = ['id', 'signature_date', 'title', 'country', 'sector', 'signed_amount']


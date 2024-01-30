from rest_framework import generics
from .serializers import CurrencyConversionSerializer
from api.models import CurrencyConversion


class ConversionRate(generics.ListCreateAPIView):
    serializer_class = CurrencyConversionSerializer

    def get_queryset(self):
        queryset = CurrencyConversion.objects.all()
        queryset = queryset.filter(start_currency=self.kwargs["start_currency"],
                                   target_currency=self.kwargs["target_currency"])
        return queryset

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Payout
from .serializers import PayoutSerializer
from .tasks import process_payout  # Celery задача


class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payout = serializer.save()

        process_payout.delay(payout.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        payout = self.get_object()

        if not payout.can_be_deleted():
            return Response(
                {"error": "Нельзя удалить выплату в текущем статусе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(payout)
        return Response(status=status.HTTP_204_NO_CONTENT)
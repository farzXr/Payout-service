from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Payout
from .serializers import PayoutSerializer
from .tasks import process_payout
import logging, os

logger = logging.getLogger("payout-api")
if not logger.handlers:
    log_dir = "/app/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler("/app/logs/api.log")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Новый запрос на создание выплаты")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            payout = serializer.save()
            logger.info(f"Создана выплата #{payout.id}")

            process_payout.delay(payout.id)
            logger.info(f"Задача Celery отправлена для выплаты #{payout.id}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"Невалидные данные: {serializer.errors}")
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        payout = self.get_object()

        if not payout.can_be_deleted():
            logger.warning(f"Нельзя удалить выплату #{payout.id} (статус: {payout.status})")
            return Response(
                {"error": "Нельзя удалить выплату в текущем статусе"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_destroy(payout)
        logger.info(f"Удаляем выплату #{payout.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

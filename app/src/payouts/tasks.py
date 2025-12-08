# tasks.py
from celery import shared_task
from django.db import transaction
from django.db.utils import OperationalError
import time
import logging
from .models import Payout, PayoutStatus

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_payout(self, payout_id):
    try:
        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)

            if payout.status != PayoutStatus.PENDING:
                logger.warning(f"Payout {payout_id} is already in {payout.status} status")
                return

            payout.mark_as_processing()
            time.sleep(5)

            import random
            if random.random() < 0.1:
                raise Exception("Random processing error")

            payout.mark_as_completed()
            logger.info(f"Payout {payout_id} processed successfully")

    except OperationalError as e:
        logger.error(f"Database error processing payout {payout_id}: {e}")
    except Payout.DoesNotExist:
        logger.error(f"Payout {payout_id} not found")
    except Exception as e:
        logger.error(f"Error processing payout {payout_id}: {e}")
        payout.mark_as_failed()
# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from .models import Payout, PayoutStatus


class PayoutModelTests(TestCase):
    def test_can_be_deleted(self):
        payout = Payout.objects.create(
            amount=100,
            currency='RUB',
            recipient_details={'account_holder': 'Test'},
            status=PayoutStatus.PENDING
        )
        self.assertTrue(payout.can_be_deleted())

        payout.status = PayoutStatus.COMPLETED
        self.assertFalse(payout.can_be_deleted())


class PayoutAPITests(APITestCase):
    def setUp(self):
        self.payout_data = {
            'amount': '100.00',
            'currency': 'RUB',
            'recipient_details': {'account_holder': 'John Doe'},
            'description': 'Test payout'
        }

        self.existing_payout = Payout.objects.create(
            amount=200,
            currency='USD',
            recipient_details={'account_holder': 'Existing User'},
            description='Existing payout'
        )

    # 1. POST /api/payouts/ — создание новой заявки
    @patch('payouts.tasks.process_payout.delay')
    def test_create_payout(self, mock_task):
        """Тестируем создание выплаты"""
        url = reverse('payout-list')
        response = self.client.post(url, self.payout_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payout.objects.count(), 2)
        mock_task.assert_called_once()

    # 2. GET /api/payouts/ — список заявок
    def test_get_payouts_list(self):
        """Тестируем получение списка выплат"""
        url = reverse('payout-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    # 3. GET /api/payouts/{id}/ — получение заявки по ID
    def test_get_payout_detail(self):
        """Тестируем получение одной выплаты"""
        url = reverse('payout-detail', args=[self.existing_payout.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.existing_payout.id)
        self.assertEqual(response.data['amount'], '200.00')

    def test_get_nonexistent_payout(self):
        """Тестируем получение несуществующей выплаты"""
        url = reverse('payout-detail', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # 4. PATCH /api/payouts/{id}/ — обновление заявки
    def test_update_payout_description(self):
        """Тестируем обновление описания выплаты"""
        url = reverse('payout-detail', args=[self.existing_payout.id])
        update_data = {'description': 'Updated description'}

        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.existing_payout.refresh_from_db()
        self.assertEqual(self.existing_payout.description, 'Updated description')

    def test_update_nonexistent_payout(self):
        """Пытаемся обновить несуществующую выплату"""
        url = reverse('payout-detail', args=[999])
        response = self.client.patch(url, {'description': 'test'}, format='json')

        self.assertEqual(response.status_code, 404)

    # 5. DELETE /api/payouts/{id}/ — удаление заявки
    def test_delete_payout(self):
        """Тестируем удаление выплаты в статусе PENDING"""
        url = reverse('payout-detail', args=[self.existing_payout.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Payout.objects.count(), 0)

    def test_delete_payout_not_allowed(self):
        """Тестируем попытку удалить выплату в статусе COMPLETED"""
        completed_payout = Payout.objects.create(
            amount=300,
            currency='EUR',
            recipient_details={'account_holder': 'Completed User'},
            status=PayoutStatus.COMPLETED
        )

        url = reverse('payout-detail', args=[completed_payout.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(Payout.objects.count(), 2)
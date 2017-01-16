from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class RedeemedDeleteTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)
        self.user2 = u.objects.create_user('user1', 'me1@snow.com', self.PW)

        with self.settings(ROOT_URLCONF='coupons.urls'):

            coupon = {
                'code': 'ASDF',
                'type': 'percent',
            }

            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.coupon_id = response.data['id']
            self.logout()

            self.login(username='user')
            response = self.client.put('/coupon/%s/redeem' % self.coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='user1')
            response = self.client.put('/coupon/%s/redeem' % self.coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='admin')
            response = self.client.get('/coupon/%s/redeemed' % self.coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))
            self.redeemed_id = response.data[0]['id']
            self.redeemed_id_2 = response.data[1]['id']
            self.logout()

    def test_can_delete_redeemed(self):
        """
        Verify admins can delete redeemed.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='admin')
            response = self.client.delete('/redeemed/%s' % self.redeemed_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.logout()

    def test_cant_delete_redeemed(self):
        """
        Verify users can't delete redeemed.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='user')
            response = self.client.delete('/redeemed/%s' % self.redeemed_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)

            response = self.client.delete('/redeemed/%s' % self.redeemed_id_2, format='json')
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.logout()

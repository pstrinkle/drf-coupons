from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponRetrieveTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()
            coupon['repeat'] = 0
            coupon['bound'] = False

            self.verify_built(coupon, response.data)

            self.coupon_id = response.data['id']

    def test_can_retrieve_coupon(self):
        """
        Verify we can retrieve a coupon.  By default, anyone can.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='user')
            response = self.client.get('/coupon/%s' % self.coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.coupon_id, response.data['id'])
            self.logout()

    def test_can_retrieve_coupon_code(self):
        """
        Verify we can retrieve a coupon by code (mixed case is fine).
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='user')
            response = self.client.get('/coupon/%s' % 'AsDf', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.coupon_id, response.data['id'])
            self.logout()



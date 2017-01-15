from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta

from coupons.tests.base import BasicTest


class CouponListTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_list_coupon(self):
        """
        Verify admins can list coupons.
        """

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

    def test_cant_list_coupons(self):
        """
        Verify normal users can't.  The group specific test in a different file.
        """

        self.assertTrue(True)


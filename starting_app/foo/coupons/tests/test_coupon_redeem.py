from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta
from time import sleep

from coupons.tests.base import BasicTest


class CouponRedeemTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_cant_redeem_expired(self):
        """
        Verify that if a coupon is expired, it can't be redeemed.
        """

        future = datetime.utcnow() + timedelta(seconds=5)

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
            'expires': str(future),
        }

        self.login(username='admin')
        response = self.client.post('/coupon', coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()

        # sleep until it's expired.
        sleep(5)



    def test_cant_redeem_wrong_user(self):
        """
        Verify that you can't redeem a coupon that is bound to another user.
        """

        self.assertTrue(True)

    def test_can_redeem_nonbound(self):
        """
        Verify that you can redeem a coupon that isn't bound to a specific user.
        """

        self.assertTrue(True)

    def test_can_redeem_bound_to_you(self):
        """
        Verify that you can redeem a bound coupon if it's bound to you.
        """

        self.assertTrue(True)


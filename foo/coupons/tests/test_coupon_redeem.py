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

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            # sleep until it's expired.
            sleep(5)

            self.login(username='admin')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_cant_redeem_wrong_user(self):
        """
        Verify that you can't redeem a coupon that is bound to another user.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'bound':  True,
            'user':   self.user.id,
            'repeat': 1,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

            self.login(username='admin')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_can_redeem_nonbound(self):
        """
        Verify that you can redeem a coupon that isn't bound to a specific user.
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            self.login(username='admin')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

    def test_can_redeem_bound_to_you(self):
        """
        Verify that you can redeem a bound coupon if it's bound to you.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'bound':  True,
            'user':   self.user.id,
            'repeat': 1,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

            self.login(username='user')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

    def test_cant_redeem_beyond_repeat(self):
        """
        Verify you can't redeem a coupon more than allowed.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'repeat': 2,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']

            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            self.logout()

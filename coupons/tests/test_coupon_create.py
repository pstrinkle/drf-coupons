from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta

from coupons.tests.base import BasicTest


class CouponCreateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_create_coupon(self):
        """
        Create a coupon that is globally bound and infinite.
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

    def test_can_create_coupon_code_codel_mismatch(self):
        """
        Verify that even if you specify the lowercase version of the code when creating, it'll be ignored.
        """

        coupon = {
            'code':   'ASDF',
            'code_l': 'mismatch',
            'type':   'percent',
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

    def test_can_create_coupon_lowercase_verification(self):
        """
        Verify creating a coupon creates a lowercase version if it's identifier.
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

    def test_cant_create_coupon_duplicate_name(self):
        """
        Verify that we ensure uniqueness of coupon code.
        """

        # Create initial one.
        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        # Create duplicate.
        coupon2 = {
            'code': 'AsdF',
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

            self.login(username='admin')
            response = self.client.post('/coupon', coupon2, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_cant_create_coupon_invalid_percentage(self):
        """
        Verify you can't provide an invalid percentage.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'value':  2,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_can_create_coupon_expires(self):
        """
        Verify you can set an expiration date, but it must be in the future.
        """

        future = datetime.utcnow() + timedelta(days=14)

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
            'expires': str(future),
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

    def test_cant_create_coupon_after_expiration(self):
        """
        Verify you can't set an expiration date in the past.
        """

        past = datetime.utcnow() + timedelta(days=-1)

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
            'expires': str(past),
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_can_create_coupon_case_i(self):
        """
        Handle case I defined in the README.
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
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_can_create_coupon_case_ii(self):
        """
        Handle case II defined in the README.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'repeat': 1,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_can_create_coupon_case_iii(self):
        """
        Handle case III defined in the README.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'bound':  True,
            'user':   self.user.id,
            'repeat': 0,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_can_create_coupon_case_iv(self):
        """
        Handle case IV defined in the README.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_can_create_coupon_case_v(self):
        """
        Handle case V defined in the README.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'bound':  True,
            'user':   self.user.id,
            'repeat': 10,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_can_create_coupon_case_vi(self):
        """
        Handle case VI defined in the README.
        """

        coupon = {
            'code':   'ASDF',
            'type':   'percent',
            'repeat': 10,
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)


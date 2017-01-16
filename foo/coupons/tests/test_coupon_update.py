from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponUpdateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_update_coupon(self):
        """
        Verify we can update a coupon.
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

            coupon['repeat'] = 50
            self.login(username='admin')
            response = self.client.put('/coupon/%s' % response.data['id'], coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.logout()

            self.verify_built(coupon, response.data)

    def test_can_update_coupon_lowercase_verification(self):
        """
        Verify if we update the coupon code, its lowercase version is updated.
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

            coupon['code'] = 'PERSON'
            del coupon['code_l']
            self.login(username='admin')
            response = self.client.put('/coupon/%s' % response.data['id'], coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_update_ignores_code_lowercase(self):
        """
        Verify if you try to update the lowercase code value, it's overwritten.
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

            # code_l doesn't match anymore.
            coupon['code'] = 'PERSON'
            self.login(username='admin')
            response = self.client.put('/coupon/%s' % response.data['id'], coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.logout()

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

    def test_cant_update_coupon_duplicate_name(self):
        """
        Verify you can't update the coupon code to become a duplicate.
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        coupon2 = {
            'code': 'SECOND',
            'type': 'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            # First coupon
            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()
            coupon_id = response.data['id']

            coupon['code_l'] = coupon['code'].lower()
            self.verify_built(coupon, response.data)

            # Second coupon
            self.login(username='admin')
            response = self.client.post('/coupon', coupon2, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            coupon2['code_l'] = coupon2['code'].lower()
            self.verify_built(coupon2, response.data)

            # Update first coupon to be the same as the second.
            coupon['code'] = 'SECOND'
            self.login(username='admin')
            response = self.client.put('/coupon/%s' % coupon_id, coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.logout()

    def test_can_update_coupon_change_binding(self):
        # XXX: Verify we can update a coupon from bound to not bound, and vice versa.

        self.assertTrue(True)

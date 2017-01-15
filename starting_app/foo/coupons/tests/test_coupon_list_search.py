from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponListSearchTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_search_coupon(self):
        """
        Verify admins can search coupons.
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            coupon['code_l'] = coupon['code'].lower()
            coupon['repeat'] = 0
            coupon['bound'] = False

            self.verify_built(coupon, response.data)

            coupon['code'] = 'new_one'
            del coupon['code_l']

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))

            response = self.client.get('/coupon', {'search': 'as'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            response = self.client.get('/coupon', {'search': 'AS'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            response = self.client.get('/coupon', {'search': 'NEW'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            self.logout()

    def test_cant_search_coupons(self):
        """
        Verify normal users can't.  The group specific test in a different file.
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            coupon['code_l'] = coupon['code'].lower()
            coupon['repeat'] = 0
            coupon['bound'] = False

            self.verify_built(coupon, response.data)

            coupon['code'] = 'new_one'
            del coupon['code_l']

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            coupon['code_l'] = coupon['code'].lower()

            self.verify_built(coupon, response.data)

            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))

            self.logout()

            self.login(username='user')
            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(0, len(response.data))

            response = self.client.get('/coupon', {'search': 'as'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(0, len(response.data))

            response = self.client.get('/coupon', {'search': 'AS'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(0, len(response.data))

            response = self.client.get('/coupon', {'search': 'NEW'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(0, len(response.data))

            self.logout()

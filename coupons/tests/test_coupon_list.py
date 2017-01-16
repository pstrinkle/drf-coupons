from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta

from coupons.tests.base import BasicTest


class CouponListTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)
        self.user2 = u.objects.create_user('user1', 'me1@snow.com', self.PW)

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

    def test_cant_list_coupons(self):
        """
        Verify normal users can only see those bound to them.  The group specific test in a different file.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            coupon = {
                'code': 'ASDF',
                'type': 'percent',
            }

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
            self.logout()

            self.login(username='admin')

            coupon = {
                'code': 'ASDF2',
                'type': 'percent',
                'bound': True,
                'user': self.user2.id,
                'repeat': 0,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            coupon = {
                'code': 'ASDF3',
                'type': 'percent',
                'bound': True,
                'user': self.user.id,
                'repeat': 0,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            should_find_id = response.data['id']

            coupon['code_l'] = coupon['code'].lower()
            self.verify_built(coupon, response.data)

            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(4, len(response.data))
            self.logout()

            self.login(username='user')
            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))
            self.logout()

            self.assertEqual(should_find_id, response.data[0]['id'])

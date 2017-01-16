from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponListFilterTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

        with self.settings(ROOT_URLCONF='coupons.urls'):
            self.login(username='admin')

            # create unbound coupon
            coupon = {
                'code':  'ten',
                'type':  'percent',
                'value': 0.10,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # create unbound coupon
            coupon = {
                'code':  'fifty',
                'type':  'percent',
                'value': 0.50,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # create coupon for range testing
            coupon = {
                'code': 'hundred',
                'type': 'value',
                'value': 100,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # create bound coupon
            coupon = {
                'code':  'bound_test',
                'type':  'percent',
                'value': 0.10,
                'bound': True,
                'user':  self.user.id,
            }

            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            self.logout()

    def test_can_filter_coupon(self):
        """
        Verify admins can filter coupons.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='admin')
            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(4, len(response.data))

            # filter by bound=False
            response = self.client.get('/coupon', {'bound': False}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(3, len(response.data))

            # filter by bound=True
            response = self.client.get('/coupon', {'bound': True}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            # filter by user
            response = self.client.get('/coupon', {'user': self.user.id}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            # filter by type
            response = self.client.get('/coupon', {'type': 'percent'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(3, len(response.data))

            response = self.client.get('/coupon', {'type': 'value'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            # filter by value
            response = self.client.get('/coupon', {'min_value': 0.50}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))

            response = self.client.get('/coupon', {'max_value': 0.49}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))

            response = self.client.get('/coupon', {'type': 'value', 'min_value': 0.50}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))
            self.assertEqual('value', response.data[0]['type'])
            self.assertEqual(100, int(float(response.data[0]['value'])))

            self.logout()

    def test_cant_filter_coupons(self):
        """
        Verify normal users can't.  The group specific test in a different file.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            self.login(username='admin')
            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(4, len(response.data))
            self.logout()

            self.login(username='user')
            response = self.client.get('/coupon', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            response = self.client.get('/coupon', {'type': 'value', 'min_value': 0.50}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(0, len(response.data))

            response = self.client.get('/coupon', {'type': 'percent', 'bound': True}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))

            self.logout()


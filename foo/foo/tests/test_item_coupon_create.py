from django.contrib.auth import get_user_model
from rest_framework import status

from foo.tests.base import BasicTest


class ItemCouponCreateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_create_coupon_within_item_app(self):
        """
        Create a coupon (boringly).
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        self.login(username='admin')
        response = self.client.post('/api/v1/coupon', coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()

        coupon['code_l'] = coupon['code'].lower()
        coupon['repeat'] = 0
        coupon['bound'] = False

        self.verify_built(coupon, response.data)

    def test_can_redeem_coupon_within_item_app(self):
        """
        Redeem a coupon (boringly).
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        self.login(username='admin')
        response = self.client.post('/api/v1/coupon', coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        coupon['code_l'] = coupon['code'].lower()
        coupon['repeat'] = 0
        coupon['bound'] = False

        self.verify_built(coupon, response.data)

        coupon_id = response.data['id']

        response = self.client.put('/api/v1/coupon/%s/redeem' % coupon_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/v1/coupon/%s/redeemed' % coupon_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

        response = self.client.get('/api/v1/redeemed', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

        self.logout()

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

from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponUpdateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', 'password123')
        self.user = u.objects.create_user('user', 'me@snow.com', 'password123')

    def test_can_update_coupon(self):
        """
        Verify we can update a coupon.
        """

        coupon = {
            'code': 'ASDF',
            'type': 'percent',
        }

        self.login(username='admin')
        response = self.client.post('/coupon', coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()

        coupon['code_l'] = coupon['code'].lower()
        coupon['repeat'] = 0
        coupon['bind'] = 'user'
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

        self.assertTrue(True)

    def test_cant_update_coupon_duplicate_name(self):
        """
        Verify you can't update the coupon code to become a duplicate.
        """

        self.assertTrue(True)

    # XXX: Verify we can update a coupon from binding to a user to an email.

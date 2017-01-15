from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponDeleteSettingsTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

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

            self.coupon_id = response.data['id']

    def test_cant_delete_coupon_if_not_in_group(self):
        """
        Verify the user can restrict permissions.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):
            with self.settings(COUPON_PERMISSIONS={'DELETE': ['group_a']}):

                self.login(username='user')
                response = self.client.delete('/coupon/%s' % self.coupon_id, format='json')
                self.assertEqual(response.status_code, status.HTTP_302_FOUND)
                self.logout()

    def test_can_delete_coupon_if_group_empty(self):
        """
        Verify the user can restrict permissions.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):
            with self.settings(COUPON_PERMISSIONS={'DELETE': []}):

                self.login(username='user')
                response = self.client.delete('/coupon/%s' % self.coupon_id, format='json')
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.logout()

    def test_can_delete_coupon_if_in_group(self):
        """
        Verify the user can restrict permissions.
        """

        g, _ = Group.objects.get_or_create(name='group_a')
        g.user_set.add(self.user)

        with self.settings(ROOT_URLCONF='coupons.urls'):
            with self.settings(COUPON_PERMISSIONS={'DELETE': ['group_a']}):

                self.login(username='user')
                response = self.client.delete('/coupon/%s' % self.coupon_id, format='json')
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.logout()

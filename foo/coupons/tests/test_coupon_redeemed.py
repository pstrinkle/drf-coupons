# XXX: Verify you can only see your own redeemed entries.
# XXX: Verify the admin can list all for the specific coupon.

from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponRedeemedTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)
        self.user2 = u.objects.create_user('user1', 'me1@snow.com', self.PW)

    def test_can_redeemed_list_all_users(self):
        """
        Verify that an admin can list all claims for a specific coupon.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            coupon = {
                'code': 'ASDF',
                'type': 'percent',
            }

            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            self.login(username='user')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='user1')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='admin')
            response = self.client.get('/coupon/%s/redeemed' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))
            self.logout()

    def test_can_redeemed_list_mine(self):
        """
        Verify that a user can only see their claims for a specific coupon.
        """

        with self.settings(ROOT_URLCONF='coupons.urls'):

            coupon = {
                'code': 'ASDF',
                'type': 'percent',
            }

            self.login(username='admin')
            response = self.client.post('/coupon', coupon, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            coupon_id = response.data['id']
            self.logout()

            self.login(username='user')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='user1')
            response = self.client.put('/coupon/%s/redeem' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.logout()

            self.login(username='admin')
            response = self.client.get('/coupon/%s/redeemed' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(2, len(response.data))
            self.logout()

            self.login(username='user')
            response = self.client.get('/coupon/%s/redeemed' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))
            self.assertEqual(self.user.id, response.data[0]['user'])
            self.logout()

            self.login(username='user1')
            response = self.client.get('/coupon/%s/redeemed' % coupon_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(1, len(response.data))
            self.assertEqual(self.user2.id, response.data[0]['user'])
            self.logout()


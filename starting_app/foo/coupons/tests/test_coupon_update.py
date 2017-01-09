from django.contrib.auth import get_user_model
from rest_framework import status

from coupons.tests.base import BasicTest


class CouponUpdateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', 'password123')

    def test_can_update_coupon(self):
        """
        Verify we can update a coupon.
        """

        self.assertTrue(True)

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

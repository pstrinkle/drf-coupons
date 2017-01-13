from django.contrib.auth import get_user_model
from rest_framework import status

from foo.tests.base import BasicTest


class ItemCreateTests(BasicTest):

    def setUp(self):
        u = get_user_model()
        u.objects.create_superuser('admin', 'john@snow.com', self.PW)
        self.user = u.objects.create_user('user', 'me@snow.com', self.PW)

    def test_can_create_item(self):
        """
        Create an item that is globally bound and infinite.
        """

        item = {
            'name':  'ASDF',
            'value': 0,
        }

        self.login(username='admin')
        response = self.client.post('/api/v1/item', item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()

        self.verify_built(item, response.data)



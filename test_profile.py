import unittest
from unittest import mock
from controllers import get_cart_count
from app import profile


class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or mock objects
        self.mock_user = mock.Mock()
        self.mock_shipping = mock.Mock()
        self.mock_session = {'email': 'test@example.com'}

    def test_profile_authenticated(self):
        # Mock the necessary dependencies
        mock_user_query = mock.Mock()
        mock_user_query.filter_by.return_value.first.return_value = self.mock_user
        mock_shipping_query = mock.Mock()
        mock_shipping_query.join.return_value.filter.return_value.all.return_value = [self.mock_shipping]
        mock_db = mock.Mock()
        mock_db.session = {'email': 'test@example.com'}
        mock_render_template = mock.Mock()
        mock_redirect = mock.Mock()
        mock_url_for = mock.Mock()
        mock_get_cart_count = mock.Mock(return_value=10)

        # Patch the necessary dependencies with the mocks
        with mock.patch('app.User.query', mock_user_query), \
             mock.patch('app.Shipping.query', mock_shipping_query), \
             mock.patch('app.db', mock_db), \
             mock.patch('app.render_template', mock_render_template), \
             mock.patch('app.redirect', mock_redirect), \
             mock.patch('app.url_for', mock_url_for), \
             mock.patch('app.get_cart_count', mock_get_cart_count):
            # Call the profile function
            response = profile()

        # Assert the expected behavior
        mock_user_query.filter_by.assert_called_with(email=self.mock_session['email'])
        mock_shipping_query.join.assert_called_with(mock_user_query)
        mock_shipping_query.filter.assert_called_with(mock_user_query.email == self.mock_session['email'])
        mock_render_template.assert_called_with('profile.html', user=self.mock_user, shipping_info=[self.mock_shipping], cart_count=10)
        self.assertEqual(response, mock_render_template.return_value)

    def test_profile_not_authenticated(self):
        # Mock the necessary dependencies
        mock_redirect = mock.Mock()
        mock_url_for = mock.Mock(return_value='/signin')

        # Patch the necessary dependencies with the mocks
        with mock.patch('app.redirect', mock_redirect), \
             mock.patch('app.url_for', mock_url_for):
            # Call the profile function
            response = profile()

        # Assert the expected behavior
        mock_redirect.assert_called_with('/signin')
        self.assertEqual(response, mock_redirect.return_value)


if __name__ == '__main__':
    unittest.main()

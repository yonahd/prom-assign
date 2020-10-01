import unittest
from unittest import mock
from main import get_response
from datetime import timedelta

TEST_URL = "https://github.com"


def mocked_requests_get(*args, **kwargs):
    mock_resp = mock.Mock()
    mock_resp.elapsed = timedelta(seconds=1)
    mock_resp.ok = kwargs['ok']
    return mock_resp


class TestAppMethods(unittest.TestCase):

    def test_get_response(self):
        self.assertRaises(TypeError, get_response)
        response = get_response(TEST_URL)
        self.assertIsInstance(response, dict)
        self.assertTrue(response['status'] in [0, 1])
        self.assertIsInstance(response['response_time'], float)

    @mock.patch('main.requests.get', side_effect=mocked_requests_get(ok=True))
    def test_fetch(self, mock_get):
        response = get_response(TEST_URL)
        self.assertIsInstance(response, dict)
        self.assertTrue(response['status'] == 1)

    @mock.patch('main.requests.get', side_effect=mocked_requests_get(ok=False))
    def test_fetch(self, mock_get):
        response = get_response(TEST_URL)
        self.assertIsInstance(response, dict)
        self.assertTrue(response['status'] == 0)


if __name__ == '__main__':
    unittest.main()

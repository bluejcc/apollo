from tests import BaseTest


class ViewBaseTest(BaseTest):
    def _test_get_request(self, endpoint):
        response = self.client.get(endpoint)
        self.assert200(response)
        return response


class TestRoot(ViewBaseTest):
    def test200(self):
        response = self._test_get_request('/')
        self.assertTrue('Definition' in response.data)


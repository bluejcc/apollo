import unittest

from approot import models, create_app, db


class BaseTest(unittest.TestCase):

    def __call__(self, result=None):
        self._pre_setup()
        super(BaseTest, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        print self.app.__dict__
        # now you can use flask thread locals
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()

    def init_data(self):
        pass

    def setUp(self):
        """ Reset tables """
        db.create_all()
        self.init_data()

    def tearDown(self):
        """ Clean db sesion and drop tables """
        db.session.remove()
        db.drop_all()

    def assert200(self, response):
        self.assertTrue(response.status_code == 200)

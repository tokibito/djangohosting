import unittest

import utils
import conf

class UtilsTestCase(unittest.TestCase):
    def test_split_hostname(self):
        self.assertEqual(utils.split_hostname('myproject.myname.example.com:8000'), ['myproject.myname.example.com', '8000'])

    def test_split_domain(self):
        self.assertEqual(utils.split_domain('myproject.myname.example.com'), ['myproject', 'myname', 'example', 'com'])

class ConfTestCase(unittest.TestCase):
    def test_resolver(self):
        resolver = conf.Resolver({'foo': {'bar': 123}})
        self.assertEqual(resolver.foo.bar, 123)

class DomainTestCase(unittest.TestCase):
    def test_domain(self):
        import domainmap
        settings = conf.Settings()
        self.assertEqual(domainmap.registered_domain(settings, 'tokibito.orz.hm'), 'tkhp.tokibito')

if __name__ == '__main__':
    unittest.main()

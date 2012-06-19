from unittest2 import TestCase
from parker.util import smartimport, LazyDescriptor

from mock import patch, call

class TestSmartImport(TestCase):
    def test_imports_package(self):
        """ smart import will import a package """
        importable = smartimport('parker.tests.importable')
        import parker.tests.importable
        assert importable == parker.tests.importable

    def test_imports_inner(self):
        """ smart import will import something at the top level of a package """
        Foo = smartimport('parker.tests.importable.Foo')
        import parker.tests.importable
        assert Foo == parker.tests.importable.Foo

    def test_imports_inner2(self):
        """ smart import will import something deep inside a package """
        bar = smartimport('parker.tests.importable.foo.bar')
        import parker.tests.importable
        assert bar == parker.tests.importable.foo.bar


class TestLazyDescriptor(TestCase):

    def test_None_default(self):
        class Test(object):
            attr = LazyDescriptor("attr")
        self.assertTrue(Test.attr is None)
        self.assertTrue(Test().attr is None)

    def test_default(self):
        class Test(object):
            attr = LazyDescriptor("attr", 10)
        self.assertEqual(Test().attr, 10)
        self.assertEqual(Test.attr, 10)

    def test_set(self):
        class Test(object):
            attr = LazyDescriptor("attr")
        t = Test()
        t.attr = 14
        self.assertEqual(t.attr, 14)
        Test.attr = 10
        self.assertEqual(Test.attr, 10)

    @patch("parker.util.smartimport")
    def test_imports(self, mocksi):
        class Test(object):
            attr = LazyDescriptor("attr", "path")

        Test().attr
        self.assertEqual(mocksi.call_args, call("path"))

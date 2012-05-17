from parker.util import smartimport

class TestSmartImport(object):
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

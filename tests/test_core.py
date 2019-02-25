import pytest

from pytedjmi import setup_migration


@setup_migration("tests", "0002_later")
def setup_test(apps):
    pass


@pytest.mark.django_db
@setup_test.to_migration("0003_latest")
def test_setup(*, old_apps=None, apps=None):
    pass

import pytest

from pytedjmi import migrate, cleanup


@pytest.mark.django_db
@cleanup
def test_migrations():
    migrate("tests", "0001_initial")
    migrate("tests", None)
    migrate("tests", "0002_later")

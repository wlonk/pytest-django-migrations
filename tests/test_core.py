import pytest
from unittest import mock

from pytedjmi import setup_migration, DjMiSetup, MigrationStructureError


@pytest.mark.django_db
def test_conflicting_migrations():
    with mock.patch("pytedjmi.core.MigrationExecutor") as executor:
        executor.loader.detect_conflicts.return_value = True
        setup = DjMiSetup(None, None)
        with pytest.raises(MigrationStructureError):
            setup.run_executor(None)


@setup_migration("tests", "0002_later")
def setup_test(apps):
    pass


@pytest.mark.django_db
@setup_test.to_migration("0003_latest")
def test_setup(*, old_apps=None, apps=None):
    pass

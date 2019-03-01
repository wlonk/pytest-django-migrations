import pytest
from unittest.mock import patch

from pytedjmi import migrate, cleanup, MigrationStructureError


@pytest.mark.django_db
@cleanup
def test_migrations():
    migrate("tests", "0001_initial")
    migrate("tests", None)
    migrate("tests", "0002_later")


@pytest.mark.django_db
@cleanup
def test_migration_conflicts():
    with patch("pytedjmi.core.MigrationExecutor") as executor:
        executor.loader.detect_conflicts.return_value = True
        with pytest.raises(MigrationStructureError):
            migrate("tests", "0001_initial")

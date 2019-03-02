import pytest
from unittest.mock import patch

from pytedjmi import migrate, cleanup, MigrationStructureError


@cleanup
def test_migrations(transactional_db):
    migrate("tests", "0001_initial")
    migrate("tests", None)
    migrate("tests", "0002_later")


@cleanup
def test_migration_conflicts(transactional_db):
    with patch("pytedjmi.core.MigrationExecutor") as executor:
        executor.loader.detect_conflicts.return_value = True
        with pytest.raises(MigrationStructureError):
            migrate("tests", "0001_initial")

import pytest
from unittest.mock import patch
from pytedjmi import migrate, MigrationStructureError


@pytest.mark.migrate_from("tests", "0001_initial")
def test_migrations(initial_apps):
    migrate("tests", None)
    migrate("tests", "0002_later")


@pytest.mark.migrate_from("tests", "0001_initial")
def test_migration_conflicts(initial_apps):
    with patch("django.db.migrations.executor.MigrationExecutor") as executor:
        executor.loader.detect_conflicts.return_value = True
        with pytest.raises(MigrationStructureError):
            migrate("tests", "0001_initial")

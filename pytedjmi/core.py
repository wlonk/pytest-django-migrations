import pytest
from functools import wraps

from django.db import connection, transaction


def pytest_load_initial_conftests(early_config, parser, args):
    # Register the marks
    early_config.addinivalue_line(
        "markers",
        "migrate_from(app, migration): start the database at (app, migration).",
    )


class MissingMigrationSetupError(Exception):
    pass


class MigrationStructureError(Exception):
    pass


def migrate(app=None, migration=None):
    from django.db.migrations.executor import MigrationExecutor

    with transaction.atomic():
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.loader.check_consistent_history(connection)

        # Before anything else, see if there's conflicting apps and
        # drop out hard if there are any
        if executor.loader.detect_conflicts():
            raise MigrationStructureError("Migrations have conflicts.")

        # Handle
        if app and migration:
            targets = [(app, migration)]
        elif app:
            targets = [
                key
                for key
                in executor.loader.graph.leaf_nodes()
                if key[0] == app
            ]
        else:
            targets = executor.loader.graph.leaf_nodes()

        plan = executor.migration_plan(targets)
        pre_migrate_state = executor._create_project_state(
            with_applied_migrations=True
        )
        post_migrate_state = executor.migrate(
            targets, plan=plan, state=pre_migrate_state.clone()
        )
        post_migrate_state.clear_delayed_apps_cache()
        return executor.loader.project_state(targets).apps


@pytest.fixture
def initial_apps(request, transactional_db):
    marker = request.node.get_closest_marker("migrate_from")
    if not marker:
        raise MissingMigrationSetupError
    # marker.args had better be app and migration!
    app, migration = marker.args
    connection.disable_constraint_checking()
    with transaction.atomic():
        initial_apps = migrate(app, migration)
        yield initial_apps
    migrate()

from functools import wraps

from django.db import connection, transaction
from django.db.migrations.executor import MigrationExecutor


class MigrationStructureError(Exception):
    pass


def migrate(app=None, migration=None):
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


def cleanup(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            connection.disable_constraint_checking()
            with transaction.atomic():
                return fn(*args, **kwargs)
        finally:
            migrate()

    return wrapper

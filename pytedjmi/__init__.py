from functools import wraps

from django.apps import apps
from django.db.migrations.executor import MigrationExecutor
from django.db import connection, transaction


class MigrationStructureError(Exception):
    pass


class DjMiSetup:
    def __init__(self, app, migrate_from):
        self.app = app
        self.migrate_from = migrate_from

    def decorate(self, fn):
        self.pre_run_fn = fn
        return self

    def run_executor(self, target):
        with transaction.atomic():
            executor = MigrationExecutor(connection)
            executor.loader.build_graph()  # reload.
            executor.loader.check_consistent_history(connection)
            # Before anything else, see if there's conflicting apps and
            # drop out hard if there are any
            if executor.loader.detect_conflicts():
                raise MigrationStructureError("Migrations have conflicts.")
            plan = executor.migration_plan(target)
            pre_migrate_state = executor._create_project_state(
                with_applied_migrations=True,
            )
            post_migrate_state = executor.migrate(
                target,
                plan=plan,
                state=pre_migrate_state.clone(),
            )
            post_migrate_state.clear_delayed_apps_cache()
            return executor.loader.project_state(target).apps

    def apply_migration(self, migrate_to):
        migrate_to = [(self.app, migrate_to)]
        return self.run_executor(migrate_to)

    def revert_migration(self):
        migrate_from = [(self.app, self.migrate_from)]
        return self.run_executor(migrate_from)

    def to_migration(self, migrate_to):
        def inner_decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                old_apps = self.revert_migration()
                self.pre_run_fn(old_apps)
                apps = self.apply_migration(migrate_to)
                with transaction.atomic():
                    return fn(
                        *args,
                        old_apps=old_apps,
                        apps=apps,
                        **kwargs,
                    )
            return wrapper
        return inner_decorator


def setup(app, migrate_from):
    """
    Use::

        @pytedjmi.setup("app", "starting point")
        def some_setup(apps):
            pass


        @pytest.mark.django_db
        @some_setup.to_migration("ending point")
        def test_bar(..., *, old_apps=None, apps=None, ...):
            pass
    """
    def inner_decorator(fn):
        dj_mi_setup = DjMiSetup(app, migrate_from)
        dj_mi_setup.decorate(fn)
        return dj_mi_setup
    return inner_decorator

from functools import wraps

from django.apps import apps
from django.db.migrations.executor import MigrationExecutor
from django.db import connection


class DjMiSetup:
    def __init__(self, app, migrate_from):
        self.app = app
        self.migrate_from = migrate_from

    def decorate(self, fn):
        self.pre_run_fn = fn
        return self

    def apply_migration(self, migrate_to):
        migrate_from = [(self.app, self.migrate_from)]
        migrate_to = [(self.app, migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(migrate_from).apps
        executor.migrate(migrate_to)
        return old_apps

    def revert_migration(self, migrate_to):
        migrate_from = [(self.app, self.migrate_from)]
        migrate_to = [(self.app, migrate_to)]
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(migrate_from)
        return executor.loader.project_state(self.migrate_to).apps

    def to_migration(self, migrate_to):
        def inner_decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    old_apps = self.revert_migration(migrate_to)
                    self.pre_run_fn(old_apps)
                    apps = self.apply_migration(migrate_to)
                    return fn(*args, apps=apps, **kwargs)
                finally:
                    self.revert_migration(migrate_to)
            return wrapper
        return inner_decorator


def setup(app, migrate_from):
    """
    Use::

        @pytedjmi.setup("app", "starting point")
        def some_setup(apps):
            pass


        @some_setup.to_migration("ending point")
        def test_bar(..., *, apps=None, ...):
            pass
    """
    def inner_decorator(fn):
        dj_mi_setup = DjMiSetup(app, migrate_from)
        dj_mi_setup.decorate(fn)
        return dj_mi_setup
    return inner_decorator

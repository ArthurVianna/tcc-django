# flake8: noqa
class datawarehouseDatabaseRouter(object):
    """
    Determine how to route database calls for an app's models (in this case, for an app named Example).
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on Example app models to `example_db`."""
        # debug purposes
        # print("read " + model._meta.app_label)
        if model._meta.app_label == 'datawarehouseManager':
            return 'datawarehouse'
        return 'default'

    def db_for_write(self, model, **hints):
        """Send all write operations on Example app models to `example_db`."""
        # debug purposes
        # print("write " + model._meta.app_label)
        if model._meta.app_label == 'datawarehouseManager':
            return 'datawarehouse'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the Example app.
        # debug purposes
        # print("obj1" + obj1._meta.app_label)
        # print("obj2" + obj2._meta.app_label)
        if obj1._meta.app_label == 'datawarehouseManager' and obj2._meta.app_label == 'datawarehouseManager':
            return True
        # No opinion if neither object is in the Example app (defer to default or other routers).
        elif 'datawarehouseManager' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the Example app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        # debug purposes
        # print(app_label)
        # print(db)
        if app_label == 'datawarehouseManager':
            # The Example app should be migrated only on the example_db database.
            return db == 'datawarehouse'
        elif db == 'datawarehouse':
            # Ensure that all other apps don't get migrated on the example_db database.
            return False

        # No opinion for all other scenarios
        return None

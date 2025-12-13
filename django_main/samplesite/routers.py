class MainRouter:
    # Перечень приложений, чьи модели следует хранить в базе utility
    route_app_labels = {'admin', 'auth', 'contenttypes', 'sessions'}
    db = 'utility'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Если приложение, которому принадлежит модель, вносящая изменения
        # в базу данных, входит в перечень из атрибута route_app_label,
        # разрешаем вносить эти изменения только в том случае, если
        # выполняется миграция в базу utility
        if app_label in self.route_app_labels:
            return db == self.db
        else:
            # В противном случае разрешаем вносить изменения в базу, только
            # если производится миграция в базу default
            return db != self.db

    def db_for_read(self, model, **hints):
        # Если приложение, к которому принадлежит заданная модель, входит
        # в перечень из атрибута route_app_label, указываем выбрать базу
        # utility, в противном случае — базу default
        if model._meta.app_label in self.route_app_labels:
            return self.db
        else:
            return None

    def db_for_write(self, model, **hints):
        # Здесь то же самое
        if model._meta.app_label in self.route_app_labels:
            return self.db
        else:
            return None

    def allow_relation(self, obj1, obj2, **hints):
        # Если обе записи принадлежат моделям из приложений, входящих
        # в перечень route_app_label, или, наоборот, обе записи принадлежат
        # моделям из приложений, не входящих в перечень route_app_label,
        # разрешаем установление связи, в противном случае — запрещаем
        if ((obj1._meta.app_label in self.route_app_labels and
             obj2._meta.app_label in self.route_app_labels) or
                (obj1._meta.app_label not in self.route_app_labels and
                 obj2._meta.app_label not in self.route_app_labels)):
            return True
        else:
            return False
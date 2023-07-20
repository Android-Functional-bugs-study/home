
import logging
import os

from androguard.core.bytecodes.apk import APK


class App(object):

    def __init__(self, app_path, root_path, app_name):
        print("Root path:", root_path)
        assert app_path is not None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app_path = app_path

        self.apk = APK(self.app_path)
        self.package_name = self.apk.get_package()
        self.main_activity = self.apk.get_main_activity()
        self.permissions = self.apk.get_permissions()
        self.activities = self.apk.get_activities()
        if app_name is not None:
            self.app_name = app_name
        else:
            self.app_name = self.apk.get_app_name()
        print("Main activity:", self.main_activity)
        print("Package name:", self.package_name)
        self.output_path = os.path.join(root_path, self.package_name)

    def get_package_name(self):
        return self.package_name

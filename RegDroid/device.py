
import os
import subprocess
import time
from threading import Thread

import uiautomator2 as u2


class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class Device(object):
    """
    Record the information of the device
    """

    def __init__(self, device_num=None, device_serial=None, is_emulator=True, rest_interval=None):
        self.device_num = device_num
        self.device_serial = device_serial
        self.is_emulator = is_emulator
        self.use = None
        self.state = None
        self.last_state = None
        self.strategy = "screen"
        self.crash_logcat = ""
        self.last_crash_logcat = ""
        self.language = "en"
        self.rest_interval = rest_interval
        self.wifi_state = True
        self.gps_state = True
        self.sound_state = True
        self.battery_state = False
        self.game_mode = True
        self.blue_light = False
        self.notification = True
        self.permission = True
        self.hourformat = "12h"

    def set_strategy(self, strategy):
        self.strategy = strategy
        self.error_num = 0
        self.wrong_num = 0

    def set_thread(self, execute_event, args):
        if execute_event is not None:
            self.thread = MyThread(execute_event, args)
        else:
            self.thread = None

    def restart(self, emulator_path, emulator_name):
        port = self.device_serial[self.device_serial.find("-") + 1 :]
        print(f"----{port}")
        subprocess.run(["adb", "-s", self.device_serial,
                       "emu", "kill"], stdout=subprocess.PIPE)
        time.sleep(self.rest_interval*20)
        os.popen(f"{emulator_path} -avd {emulator_name} -read-only -port {port}")
        print("wait-for-device")
        subprocess.run(["adb", "-s", self.device_serial,
                       "wait-for-device"], stdout=subprocess.PIPE)
        print("wait-for-device end")
        time.sleep(self.rest_interval*10)

    def make_strategy(self, root_path):
        if not os.path.isdir(f"{root_path}strategy_{self.strategy}/"):
            os.makedirs(f"{root_path}strategy_{self.strategy}/")
        self.f_error = open(
            f"{root_path}strategy_{self.strategy}/error_realtime.txt",
            'w',
            encoding='utf-8',
        )
        self.f_wrong = open(
            f"{root_path}strategy_{self.strategy}/wrong_realtime.txt",
            'w',
            encoding='utf-8',
        )

    def make_strategy_runcount(self, run_count, root_path):
        self.path = f"{root_path}strategy_{self.strategy}/{str(run_count)}/"
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if not os.path.isdir(f"{self.path}screen/"):
            os.makedirs(f"{self.path}screen/")
        self.f_read_trace = open(f'{self.path}/read_trace.txt', 'w', encoding='utf-8')
        self.f_trace = open(f'{self.path}/trace.txt', 'w', encoding='utf-8')

        self.error_event_lists = []
        self.wrong_event_lists = []
        self.wrong_flag = True

    def connect(self):
        self.use = u2.connect_usb(self.device_serial)
        self.use.implicitly_wait(5.0)

    def install_app(self, app):
        print(app)
        subprocess.run(["adb", "-s", self.device_serial,
                       "install", app], stdout=subprocess.PIPE)

    def initialization(self):
        self.use.set_orientation("n")

    def initial_setting(self):
        print("initial setting")

    def screenshot_and_getstate(self, path, event_count):
        self.screenshot_path = path + \
                str(event_count)+'_'+self.device_serial+'.png'
        self.use.screenshot(path+str(event_count)+'_' +
                            self.device_serial+'.png')
        xml = self.use.dump_hierarchy()
        f = open(path+str(event_count)+'_'+self.device_serial +
                 '.xml', 'w', encoding='utf-8')
        f.write(xml)
        with open(path+str(event_count)+'_'+self.device_serial +
                 '.xml', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    def update_state(self, state):
        self.last_state = self.state
        self.state = state

    def stop_app(self, app):
        self.use.app_stop(app.package_name)

    def clear_app(self, app, is_login_app):
        if is_login_app == 0:
            self.use.app_stop(app.package_name)
        else:
            self.use.app_clear(app.package_name)

    def start_app(self, app):
        self.use.app_start(app.package_name)
        subprocess.run(
            [
                "adb",
                "-s",
                self.device_serial,
                "shell",
                "am",
                "start",
                "-n",
                f"{app.package_name}/{app.main_activity}",
            ],
            stdout=subprocess.PIPE,
        )
        # self.use.app_wait(app.package_name, front=True, timeout=2.0)
        return True

    def click(self, view, strategy_list):
        try:
            if self.strategy != "language":
                if view.description != "":
                    self.use(description=view.description,
                             packageName=view.package).click()
                    return "description"
                elif view.text != "":
                    self.use(text=view.text, packageName=view.package).click()
                    return "text"
                elif view.instance == 0:
                    self.use(className=view.className, resourceId=view.resourceId,
                             packageName=view.package).click()
                    return "classNameresourceId"
                else:
                    self.use.click(view.x, view.y)
                    return "xy"
            elif view.instance == 0:
                self.use(className=view.className, resourceId=view.resourceId,
                         packageName=view.package).click()
                return "classNameresourceId"
            else:
                self.use.click(view.x, view.y)
                return "xy"
        except:
            self.use.click(view.x, view.y)
            return "xy"

    def _click(self, view, text):
        try:
            if text is not None and view.text == text:
                self.use(text=view.text, packageName=view.package).click()
                return "text"
            if view.description != "":
                self.use(description=view.description,
                         packageName=view.package).click()
                return "description"
            elif view.instance == 0:
                self.use(className=view.className, resourceId=view.resourceId,
                         packageName=view.package).click()
                return "classNameresourceId"
            else:
                self.use.click(view.x, view.y)
                return "xy"
        except:
            self.use.click(view.x, view.y)
            return "xy"

    def longclick(self, view, strategy_list):
        try:
            if self.strategy != "language":
                if view.description != "":
                    self.use(description=view.description,
                             packageName=view.package).long_click(duration=1.0)
                    return
                elif view.text != "":
                    self.use(text=view.text, packageName=view.package).long_click(
                        duration=1.0)
                    return
                elif view.instance == 0:
                    self.use(className=view.className, resourceId=view.resourceId,
                             packageName=view.package).long_click(duration=1.0)
                else:
                    self.use.long_click(view.x, view.y, duration=1.0)
            elif view.instance == 0:
                self.use(className=view.className, resourceId=view.resourceId,
                         packageName=view.package).long_click(duration=1.0)
            else:
                self.use.long_click(view.x, view.y, duration=1.0)
        except:
            self.use.long_click(view.x, view.y, duration=1.0)
            # print("x:"+str(view.x)+",y:"+str(view.y))
            return

    def edit(self, view, strategy_list, text):
        if "language" not in strategy_list:
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).set_text(text)
        else:
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).set_text(text)

    def scroll(self, view, strategy_list):
        if view.action == "scroll_backward":
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).scroll.vert.backward(steps=100)
        elif view.action == "scroll_forward":
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).scroll.vert.forward(steps=100)
        elif view.action == "scroll_right":
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).scroll.horiz.toEnd(max_swipes=10)
        elif view.action == "scroll_left":
            self.use(className=view.className, resourceId=view.resourceId,
                     packageName=view.package).scroll.horiz.toBeginning(max_swipes=10)

    def close_keyboard(self):
        subprocess.run(["adb", "-s", self.device_serial, "shell",
                       "input", "keyevent", "111"], stdout=subprocess.PIPE)

    def add_file(self, resource_path, resource, path):
        subprocess.run(["adb", "-s", self.device_serial,
                       "logcat", "-c"], stdout=subprocess.PIPE)
        subprocess.run(
            [
                "adb",
                "-s",
                self.device_serial,
                "push",
                f"{resource_path}/{resource}",
                path,
            ],
            stdout=subprocess.PIPE,
        )

    def log_crash(self, path):
        os.popen(f"adb -s {self.device_serial} logcat -b crash >{path}")

    def mkdir(self, path):
        subprocess.run(["adb", "-s", self.device_serial, "shell",
                       "mkdir", path], stdout=subprocess.PIPE)

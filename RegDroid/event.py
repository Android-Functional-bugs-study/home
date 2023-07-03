
import traceback


class Event(object):

    def __init__(self, view, action, device, event_count):
        self.view = view
        self.action = action
        self.device = device
        self.text = "None"
        self.count = 0
        self.event_count = event_count

    def set_device(self, device):
        self.device = device

    def set_text(self, text):
        self.text = text

    def set_count(self, count):
        self.count = count

    def print_event(self):
        try:
            print("Event start=============================")
            print(f"Event_count:{str(self.event_count)}")
            if self.view is not None:
                print(f"View_text:{self.view.line}")
            print(f"Action:{self.action}")
            print(f"Device:{self.device.device_serial}")
            if self.text is not None:
                print(f"Text:{self.text}")
            print("Event end=============================")
        except Exception:
            traceback.print_exc()

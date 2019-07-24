from event_handler import EventHandler, BaseEvent
import time

class GSheetsEvent(BaseEvent):
    def __init__(self, data):
        super().__init__(data)

class TimerEvent(BaseEvent):
    def __init__(self, data):
        super().__init__(data)


modules_conf_filepath = './conf_files/modules.ini'
user_conf_filepath = './conf_files/config.ini'


def gsheets_listener(modules, storage, config, aggregator):
    gsheets = modules['GoogleSheetsClient']

    spreadsheet = gsheets.open_spreadsheet(config['GSheetsSettings']['sheet_name'])
    worksheet = spreadsheet.sheet1
    data = gsheets.get_all_data(worksheet)

    while True:
        new_data = gsheets.get_all_data(worksheet)
        if new_data != data:
            event = GSheetsEvent(new_data[len(data):])
            aggregator.put_event(event)
        time.sleep(15)


def timer_listener(modules, storage, config, aggregator):
    while True:
        for i in range(10):
            event = TimerEvent(i)
            aggregator.put_event(event)
        time.sleep(10)

def printer1(modules, storage, config, event):
    time.sleep(1)
    print('Printer1:', event.data)

def printer2(modules, storage, config, event):
    time.sleep(2)
    print('Printer2:', event.data)


def main():
    handler = EventHandler()

    handler.add_threaded_function(gsheets_listener)
    handler.add_threaded_function(timer_listener)
    handler.register_action(GSheetsEvent(None).type, printer1) #WTF? Needa change event type handling
    handler.register_action(TimerEvent(None).type, printer1)
    handler.register_action(TimerEvent(None).type, printer2)

    handler.start(modules_conf_filepath, user_conf_filepath, max_workers=3)

if __name__ == '__main__':
    main()
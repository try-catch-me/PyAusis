import json
import time
import datetime

from pick import pick
from colorama import Fore
from pytimeparse.timeparse import timeparse

from plugin import plugin
from core.textParser import parse_date


"""
Module content:
* RemindTodoBase: Shared functionality between Remind and Todo

* TododBase:  Based on RemindTodoBase; implements functionality required for
              RemindTodoBase to work
* RemindBase: Based on RemindTodoBase; implements functionality required for
              RemindTodoBase to work PLUS other functionality

* RemindTodoInteract_Todo:   Used by TodoBase to access Remind
* RemindTodoInteract_Remind: Used by RemindBase to access Todo (necessary for
                             todo reminders)

* Plugins (Todo, Todo_Add, Todo_Remove, Remind, Remind_At, Remind_In,
          Remind_Remove) - oneliner based on TodoBase and RemindBase to
          "export" functionality as Plugins
"""


class RemindTodoBase:
    def get_data(self, ausis):
        remind_todo_json = ausis.get_data(self.get_key())
        if remind_todo_json is None:
            remind_todo_json = "[]"
            ausis.add_data(self.get_key(), remind_todo_json)

        try:
            remind_todo_list = json.loads(remind_todo_json)
        except json.decoder.JSONDecodeError:
            ausis.say(
                "Could not read Remind / Todo List. Sorry, \
                        that should not have happend...", Fore.RED)
            remind_todo_json = "[]"
            ausis.update_data(self.get_key(), remind_todo_json)
            remind_todo_list = json.loads(remind_todo_json)

        remind_todo_list = self.sort(remind_todo_list)
        return remind_todo_list

    def save_data(self, ausis, remind_todo_list):
        ausis.update_data(self.get_key(), json.dumps(remind_todo_list))

    def get_next_id(self, ausis):
        next_id = ausis.get_data(self.get_key_next_id())
        if next_id is None:
            next_id = 0
            ausis.add_data(self.get_key_next_id(), next_id)

        ausis.update_data(self.get_key_next_id(), next_id + 1)
        return next_id

    def remove(self, ausis, s):
        data = self.get_data(ausis)
        if len(data) == 0:
            ausis.say("Nothing to remove!")
            return

        if s.startswith("everything") or s.startswith("all"):
            for entry in data:
                self.clean_up_entry(ausis, entry)

            data = []
            self.save_data(ausis, data)

            ausis.say("ok")
            return

        # open selection menu
        ask_str = []
        for entry in data:
            ask_str.append(self.format(ausis, entry))

        title = 'Please choose task to remove (select with space)'
        selected = pick(ask_str, title, multi_select=True)
        selected = [entry[1] for entry in selected]

        new_data = []
        for index, entry in enumerate(data):
            entry = data[index]
            if index not in selected:
                new_data.append(entry)
            else:
                self.clean_up_entry(ausis, entry)

        self.save_data(ausis, new_data)

    def modify(self, ausis, modified_entry):
        modified_id = modified_entry['id']
        data = self.get_data(ausis)
        data = [entry for entry in data if entry['id'] != modified_id]
        data.append(modified_entry)
        self.save_data(ausis, data)

    def do_print(self, ausis):
        todo_list = self.get_data(ausis)

        if len(todo_list) == 0:
            ausis.say("No entry!")
        for entry in todo_list:
            ausis.say(self.format(ausis, entry))


class TodoBase(RemindTodoBase):
    def interact(self):
        return RemindTodoInteract_Todo()

    def get_key(self):
        return "todo"

    def get_key_next_id(self):
        return "todo_next_id"

    def add(self, ausis, message, progress="", priority=-1):
        data = self.get_data(ausis)
        next_id = self.get_next_id(ausis)
        new_entry = {
            'message': message,
            'progress': progress,
            'priority': priority,
            'id': next_id
        }
        data.append(new_entry)
        self.save_data(ausis, data)

    def clean_up_entry(self, ausis, entry):
        self.interact().clean_up_entry(ausis, entry)

    def format(self, ausis, entry):
        message = entry['message']
        schedule = self.interact().format_interact(ausis, entry)
        progress = entry['progress']
        if progress != '':
            progress = ' -- {} -- '.format(progress)
        return "{}{}{}".format(message, progress, schedule)

    def sort(self, todo_list):
        return sorted(todo_list, key=lambda entry: entry['priority'])

    def select_one_remind(self, ausis):
        data = self.get_data(ausis)
        ask_str = []
        for entry in data:
            ask_str.append(self.format(ausis, entry))

        if len(ask_str) == 0:
            return None

        title = 'Please choose from todo list:'
        _, index = pick(ask_str, title)

        return data[index]


class RemindBase(RemindTodoBase):
    def interact(self):
        return RemindTodoInteract_Remind()

    def get_key(self):
        return "remind"

    def get_key_next_id(self):
        return "todo_next_id"

    def require(self):
        pass

    def alias(self):
        pass

    def complete(self):
        pass

    def first_time_init(self, ausis):
        remind_still_active = []
        for item in self.get_data(ausis):
            timestamp = item['timestamp']
            if timestamp < time.time():
                time_format = self.timestamp_to_string(timestamp)
                ausis.say(
                    "Reminder: {} missed ({})".format(
                        item['message'], time_format), Fore.MAGENTA)
                continue

            schedule_id = ausis.schedule(timestamp, self.reminder_exec,
                                          item['message'])
            item['schedule_id'] = schedule_id
            remind_still_active += [item]
        self.save_data(ausis, remind_still_active)

    def add(
            self,
            ausis,
            message,
            timestamp=None,
            schedule_id=None,
            todo_refere_id=None):
        data = self.get_data(ausis)
        next_id = self.get_next_id(ausis)
        new_entry = {
            'message': message,
            'timestamp': timestamp,
            'schedule_id': schedule_id,
            'todo_refere_id': todo_refere_id,
            'id': next_id
        }
        new_data = data + [new_entry]
        self.save_data(ausis, new_data)

    def clean_up_entry(self, ausis, entry):
        ausis.cancel(entry['schedule_id'])

    def format(self, ausis, entry):
        time = self.timestamp_to_string(entry['timestamp'])
        additional = self.interact().format_interact(ausis, entry)
        return "{} => {}{}".format(time, entry['message'], additional)

    def sort(self, remind_list):
        return sorted(remind_list, key=lambda entry: entry['timestamp'])

    def reminder_exec(self, ausis, schedule_id, message):
        ausis.notification(message)

        data = self.get_data(ausis)
        data = [entry for entry in data if entry['schedule_id'] != schedule_id]
        self.save_data(ausis, data)

    def timestamp_to_string(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

    def parse_date_timestamp(self, date):
        date = parse_date(date)
        if date[0] == 0:
            return None
        timestamp = time.mktime(date[1].timetuple())
        return timestamp - time.time()

    def remind_add(self, ausis, s, time_in_parser, example):
        s = s.split(" to ")
        if len(s) != 2:
            ausis.say("Sorry, please say something like:", Fore.MAGENTA)
            ausis.say(" > {}".format(example), Fore.MAGENTA)
            return

        time_in = time_in_parser(s[0])
        while time_in is None:
            ausis.say("Sorry, when should I remind you?", Fore.MAGENTA)
            time_in = time_in_parser(ausis.input("Time: "))
        timestamp = time.time() + time_in

        message = s[1]
        notification_message = message

        todo_refere_id = None
        if message == 'todo':
            message = ''
            todo_refere_entry = self.interact().select_one_remind(ausis)
            if todo_refere_entry is None:
                ausis.say("Nothing selected", Fore.MAGENTA)
                return
            notification_message = todo_refere_entry['message']
            notification_message = "TODO: {}".format(notification_message)
            todo_refere_id = todo_refere_entry['id']

        # schedule
        schedule_id = ausis.schedule(time_in, self.reminder_exec,
                                      notification_message)
        self.add(ausis, message, timestamp=timestamp, schedule_id=schedule_id,
                 todo_refere_id=todo_refere_id)


class RemindTodoInteract_Todo:
    def __init__(self):
        self.remind = RemindBase()

    def clean_up_entry(self, ausis, entry):
        todo_id = entry['id']
        remind_list = self.remind.get_data(ausis)
        remind_list_new = []
        modify = False
        for entry in remind_list:
            refere = entry['todo_refere_id']
            if refere is not None and refere == todo_id:
                self.remind.clean_up_entry(ausis, entry)
                modify = True
            else:
                remind_list_new.append(entry)

        if modify:
            self.remind.save_data(ausis, remind_list_new)

    def format_interact(self, ausis, entry):
        todo_id = entry['id']
        remind_list = self.remind.get_data(ausis)
        remind_list = [remind for remind in remind_list
                       if remind['todo_refere_id'] == todo_id]
        if len(remind_list) != 0:
            remind_list = [self.remind.timestamp_to_string(remind['timestamp'])
                           for remind in remind_list]
            return " -- remind -- ({})".format(', '.join(remind_list))
        return ''


class RemindTodoInteract_Remind:
    def __init__(self):
        self.todo = TodoBase()

    def clean_up_entry(self, ausis, entry):
        pass

    def format_interact(self, ausis, entry):
        todo_refere_id = entry['todo_refere_id']
        if todo_refere_id is not None:
            todo_list = self.todo.get_data(ausis)
            todo = [todo for todo in todo_list if todo['id'] == todo_refere_id]
            if len(todo) != 1:
                return "ERROR"
            else:
                todo = todo[0]
            return "ToDo ->-> {}".format(todo['message'])
        else:
            return ""

    def select_one_remind(self, ausis):
        return self.todo.select_one_remind(ausis)


# ##################### PLUGIN DEFINITION ##########################
@plugin('todo')
class Todo(TodoBase):
    """
    List todo list
    Note: Use
    - remind in 5 minutes to todo
    - remind at 12:30 to todo
    To select todo-entry and receive notification.
    """

    def __call__(self, ausis, s):
        self.do_print(ausis)


@plugin('todo add')
class Todo_Add(TodoBase):
    """Add new todo entry"""

    def __call__(self, ausis, s):
        self.add(ausis, s)


@plugin('todo remove')
class Todo_Remove(TodoBase):
    """
    Remove reminder
    -- Example:
        remind remove
        remind remove everything
    """

    def __call__(self, ausis, s):
        self.remove(ausis, s)


@plugin('todo progress')
class Todo_Progress(TodoBase):
    """
    Set progress info
    """

    def __call__(self, ausis, s):
        entry = self.select_one_remind(ausis)
        entry['progress'] = ausis.input("Progress: ")
        self.modify(ausis, entry)


@plugin('remind')
class Remind(RemindBase):
    """List all scheduled reminders"""

    def init(self, ausis):
        self.first_time_init(ausis)

    def __call__(self, ausis, s):
        ausis.say("## {} ##\n".format(self.timestamp_to_string(time.time())))
        self.do_print(ausis)


@plugin('remind at')
class Remind_At(RemindBase):
    """
    Add reminder
    -- Example:
        Remind at 12:30 to buy tomatoes
        Remind at 12:30 to todo
    """

    def __call__(self, ausis, s):
        self.remind_add(ausis, s, self.parse_date_timestamp,
                        'remind at 12:30 to XXX')


@plugin('remind in')
class Remind_In(RemindBase):
    """
    Add reminder
    -- Example:
        remind in 30 minutes 10 seconds to buy tomatoes
        remind in 30 minutes 10 seconds to todo
    """

    def __call__(self, ausis, s):
        self.remind_add(ausis, s, timeparse, 'remind in 30m 10s to XXX')


@plugin('remind remove')
class Remind_Remove(RemindBase):
    """
    -- Example:
        remove
        remove everything
    """

    def __call__(self, ausis, s):
        self.remove(ausis, s)

import calendar
from datetime import date, datetime, timedelta
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.properties import DictProperty
import json


tasks_list = ['Walk the dog', 'Moms Birthday', "Ship shoes at store"]
session_data = DictProperty({})
session_data = {'cur_day': datetime.now().day}

# label_month = Label(text=f"{calendar.month_name[self.month]}")
# self.month = datetime.now().month

# screen where user opens app at
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        #create wigdets
        label = Label(text='Hello U$er')
        button_cal = Button(text='Calendar',
                            size_hint=(.5, .25), pos_hint={'center_x': 0.5})
        button_today_tasks = Button(text="Todays Tasks",
                            size_hint=(.5, .25), pos_hint={'center_x': 0.5})

        # Binding buttons
        button_cal.bind(on_press=self.display_calendar)
        button_today_tasks.bind(on_press=self.display_tasks)


        #Add widgets to layout
        layout.add_widget(label)
        layout.add_widget(button_cal)
        layout.add_widget(button_today_tasks)

        self.add_widget(layout)

    def display_tasks(self, instance):
        self.manager.current = 'tasks'

    def display_calendar(self, instance):
        self.manager.current = 'calender'

# displays events if anything exists for the day selected
class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        with open('september.json', 'r') as file:
            self.month_data = json.load(file)


        # creating widgets for screen/layout
        image_logo = Image(source='pencil.png', size_hint=(1.2, 1.2), pos_hint={'center_x': 0.5})
        button_back = Button(text='Back to main screen',
                            size_hint=(.3, .1), pos_hint={'center_x': 0.5})
        button_add_task = Button(text='Add Task', size_hint=(.3, .1), pos_hint={'center_x': 0.5})
        button_remove_tasks = Button(text='Remove Selected Tasks', size_hint=(.3, .1), pos_hint={'center_x': 0.5})

        # Create a ScrollView to contain the tasks
        scroll_view = ScrollView()
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        scroll_view.add_widget(self.tasks_layout)


        # binding buttons to functions
        button_back.bind(on_press=self.go_back)
        button_add_task.bind(on_press=self.add_task)
        button_remove_tasks.bind(on_press=self.remove_tasks)

        # position of code makes the posistion of widget in GUI
        layout.add_widget(image_logo)
        layout.add_widget(scroll_view)
        layout.add_widget(button_add_task)
        layout.add_widget(button_remove_tasks)
        layout.add_widget(button_back)

        self.add_widget(layout)

    def on_pre_enter(self):
        self.update_tasks()
        

        if str(session_data['cur_day']) in self.month_data['tasks']:
            for task in self.month_data['tasks'][str(session_data['cur_day'])]:
                task_layout = BoxLayout(size_hint_y=None, height=40)
                checkbox = CheckBox(size_hint_x=None, width=30)
                label = Label(text=task, size_hint_x=1, halign='left')
                label.bind(size=label.setter('text_size'))
                task_layout.add_widget(checkbox)
                task_layout.add_widget(label)
                self.tasks_layout.add_widget(task_layout)
                self.checkboxes.append((checkbox, task))

    def go_back(self, instance):
        self.manager.current = 'main'
    
    def add_task(self, instance):
        self.manager.current = 'addTask'
    
    def remove_tasks(self, instance):
        # First, read the current data
        with open('september.json', 'r') as file:
            self.month_data_write = json.load(file)
        
        # Modify the data
        tasks_to_remove = [task for checkbox, task in self.checkboxes if checkbox.active]
        current_day = str(session_data['cur_day'])

        if current_day in self.month_data_write['tasks']:
            self.month_data_write['tasks'][current_day] = [
                task for task in self.month_data_write['tasks'][current_day] 
                if task not in tasks_to_remove
            ]

        # Now, write the modified data back to the file
        with open('september.json', 'w') as file:
            json.dump(self.month_data_write, file, indent=2)
        
    # Update the UI
        self.update_tasks()

    def update_tasks(self):
        self.tasks_layout.clear_widgets()
        self.checkboxes = []  # Store references to checkboxes


# displays events if anything exists for the day
class AddTaskScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')


        # creating widgets for screen/layout
        image_logo = Image(source='pencil.png', size_hint=(.5, .5), pos_hint={'center_x': 0.5})
        button_back = Button(text='Back to task screen',
                            size_hint=(.3, .1), pos_hint={'center_x': 0.5})
        button_add = Button(text='Add',
                            size_hint=(.3, .1), pos_hint={'center_x': 0.5})
        self.textinput_task = TextInput(hint_text="Enter Task", multiline=False)


        # binding buttons to functions
        button_add.bind(on_press=self.add)
        button_back.bind(on_press=self.go_back_tasks)

        # position of code makes the posistion of widget in GUI
        layout.add_widget(image_logo)
        layout.add_widget(self.textinput_task)
        layout.add_widget(button_add)
        layout.add_widget(button_back)

        self.add_widget(layout)

    def add(self, instance):
        # First, read the current data
        try:
            with open('september.json', 'r') as file:
                self.month_data_write = json.load(file)
        except FileNotFoundError:
            self.month_data_write = {"tasks": {}}

        current_day = str(session_data['cur_day'])
        new_task = str(self.textinput_task.text).strip()

        # Check if the new task is not empty
        if not new_task:
            return  # Don't add empty tasks

        # Ensure 'tasks' key exists
        if 'tasks' not in self.month_data_write:
            self.month_data_write['tasks'] = {}

        # Add the task
        if current_day not in self.month_data_write['tasks']:
            self.month_data_write['tasks'][current_day] = [new_task]
        else:
            self.month_data_write['tasks'][current_day].append(new_task)

        # Write the modified data back to the file
        with open('september.json', 'w') as file:
            json.dump(self.month_data_write, file, indent=2)

        # Clear the input field
        self.textinput_task.text = ''
        
    def go_back_tasks(self, instance):
        self.manager.current = 'tasks'

# displays events if anything exists for the day
class Calender(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.month = datetime.now().month
        self.year = datetime.now().year
        self.WEEK_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        self.time_labal = Label(text=f"Current Year:\n{date.today().year}",size_hint=(1, None),
                           height='48dp',  # Adjust this value as needed
                           pos_hint={'center_x': 0.5, 'top': 1})
        self.main_layout = BoxLayout(orientation='horizontal')
        self.left_layout = BoxLayout(orientation='vertical')

        # month_spinner
        month_spinner = Spinner(text='SelectMonth',
                                values=['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'],
                    size_hint_y=None,
                    height=dp(40),
                    size_hint_x=0.8)
        
        self.left_layout.add_widget(month_spinner)


        # creating widgets for screen/layout
        button_back = Button(
            text='Back to main screen',
            size_hint_y=None,
              height=dp(40),
              size_hint_x=0.8)
                    

        # binding buttons to functions
        button_back.bind(on_press=self.go_back_main)
        self.left_layout.add_widget(button_back)


        self.right_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        self.create_calendar()

    def create_calendar(self):
        days_layout = GridLayout(cols=7, size_hint_y=0.1)

        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            days_layout.add_widget(Label(text=day))

        
        label_month = Label(text=f"{calendar.month_name[self.month]}")

        self.right_layout.add_widget(label_month)
        self.right_layout.add_widget(days_layout)

        # calendar grid
        calendar_grid = GridLayout(cols=7)

        # used to get the first day of the month
        first_day = datetime(self.year, self.month, 1)
        days_in_month = (datetime(self.year, self.month % 12 + 1, 1) - timedelta(days=1)).day

        for _ in range(first_day.weekday()):
            calendar_grid.add_widget(Label(text=""))
        
        with open('september.json', 'r') as file:
            self.month_data = json.load(file)


        # Add buttons for each day          
        for day in range(1, days_in_month + 1):
            btn = Button(text=str(day))
            if str(day) in self.month_data['tasks'] and (len(self.month_data['tasks'][str(day)]) != 0):
                btn.background_color = [1, 0, 0, 1]

            btn.bind(on_press=self.on_day_press)

            calendar_grid.add_widget(btn)
        
        

        self.right_layout.add_widget(calendar_grid)


        calendar_title = Label(
            text='Calendar',
            size_hint_y=None,
            height='48dp'
        )
        self.right_layout.add_widget(calendar_title)

        self.main_layout.add_widget(self.left_layout)
        self.main_layout.add_widget(self.right_layout)
    
        self.add_widget(self.time_labal)
        self.add_widget(self.main_layout)

    def on_day_press(self, instance):
        self.day_number = int(instance.text)
        session_data['cur_day'] = self.day_number
        self.manager.current = 'tasks'

    def go_back_main(self, instance):
        self.manager.current = 'main'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TasksScreen(name='tasks'))
        sm.add_widget(AddTaskScreen(name='addTask'))
        sm.add_widget(Calender(name='calender'))
        return sm



if __name__ == '__main__':
    MyApp().run()
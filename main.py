import calendar
from datetime import date
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

tasks_list = ['Walk the dog', 'Moms Birthday', "Ship shoes at store"]

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

# displays events if anything exists for the day
class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')


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
    
    def update_tasks(self):
        self.tasks_layout.clear_widgets()
        self.checkboxes = []  # Store references to checkboxes
        for task in tasks_list:
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
        global tasks_list
        task_to_remove = [task for checkbox, task in self.checkboxes if checkbox.active]
        for task in task_to_remove:
            tasks_list.remove(task)
        self.update_tasks()
        


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
        tasks_list.append(self.textinput_task.text)

    def go_back_tasks(self, instance):
        self.manager.current = 'tasks'


# displays events if anything exists for the day
class Calender(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        time_labal = Label(text=f"Current Year:\n{date.today().year}",size_hint=(1, None),
                           height='48dp',  # Adjust this value as needed
                           pos_hint={'center_x': 0.5, 'top': 1})
        main_layout = BoxLayout(orientation='horizontal')
        left_layout = BoxLayout(orientation='vertical')

        # month_spinner
        month_spinner = Spinner(text='SelectMonth',
                                values=['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'],
                    size_hint_y=None,
                    height=dp(40),
                    size_hint_x=0.8)
        
        left_layout.add_widget(month_spinner)


        # creating widgets for screen/layout
        button_back = Button(
            text='Back to main screen',
            size_hint_y=None,
              height=dp(40),
              size_hint_x=0.8)
                    

        # binding buttons to functions
        button_back.bind(on_press=self.go_back_main)
        left_layout.add_widget(button_back)

        right_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)

        calendar_title = Label(
            text='Calendar',
            size_hint_y=None,
            height='48dp'
        )
        self.calendar_display = Label(
            text=calendar.month(date.today().year, date.today().month),
            size_hint=(None, None),
            size=(dp(500), dp(400)),  # Adjust these values as needed
            text_size=(dp(300), dp(250)),  # This makes the text wrap within the label
            halign='left',
            valign='top',
            font_name='RobotoMono-Regular'  # Use a monospaced font if available
        )

        right_layout.add_widget(self.calendar_display)
        right_layout.add_widget(calendar_title)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
    
        self.add_widget(time_labal)
        self.add_widget(main_layout)

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
import time
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Progress: 0")
        self.button = Button(text="Start Task")
        self.button.bind(on_press=self.start_task)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        return self.layout

    def start_task(self, instance):
        # Start worker in background
        thread = threading.Thread(target=self.worker)
        thread.start()

    def worker(self):
        for i in range(1, 6):
            time.sleep(1)
            # schedule update on the main thread
            Clock.schedule_once(lambda dt, val=i: self.update_label(val))

    def update_label(self, value):
        self.label.text = f"Progress: {value}"


if __name__ == "__main__":
    MyApp().run()

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import os
import socket_client
#kivy.require('1.10.1')


class ConnectPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 2

		self.add_widget(Label(text="IP:"))

		self.ip = TextInput(multiline=False)
		self.add_widget(self.ip)


		self.add_widget(Label(text="Port:"))

		self.port = TextInput(multiline=False)
		self.add_widget(self.port)


		self.add_widget(Label(text="Username:"))

		self.username = TextInput(multiline=False)
		self.add_widget(self.username)

		self.join = Button(text="Join")
		self.join.bind(on_press=self.join_button)
		self.add_widget(Label())
		self.add_widget(self.join)

	def join_button(self, instance):
		port = self.port.text
		ip = self.ip.text
		username = self.username.text

		info = f"Attempting to join {ip}:{port} as {username}"
		chat_app.info_page.update_info(info)
		chat_app.screen_manager.current = "Info"
		Clock.schudule_once(self.connect, 1)

	def connect(self, _):
		port = self.port
		ip = self.ip
		username = self.username

		if not socket_client.connect(ip, port, username, show_error):
			return

		chat_app.create_caht_page()
		chat_app.screen_manager.current = "chat"




class InfoPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 1
		self.message = Label(halign="center", valign="middle", font_size=30)
		self.message.bind(width=self.update_text_width)
		self.add_widget(self.message)

	def update_info(self, message):
		self.message.text = message

	def update_text_width(self, *_):
		self.message.text_size = (self.message.width*0.9, None)
		


class MobApp(App):
	def build(self):
		self.screen_manager = ScreenManager()

		self.connect_page = ConnectPage()
		screen = Screen(name='Connect')
		screen.add_widget(self.connect_page)
		self.screen_manager.add_widget(screen)


		self.info_page = InfoPage()
		screen = Screen(name='Info')
		screen.add_widget(self.info_page)
		self.screen_manager.add_widget(screen)

		return self.screen_manager

if __name__ == "__main__":
	chat_app = MobApp()
	chat_app.run()
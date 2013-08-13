from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty  # at top of file
from sleekxmpp import ClientXMPP  # at the top of the file
 
class AccountDetailsForm(AnchorLayout):
    server_box = ObjectProperty()
    username_box = ObjectProperty()
    password_box = ObjectProperty()

    def login(self):
        print(self.server_box.text)
        print(self.username_box.text)
        print(self.password_box.text)

        print("Click the goddamn button")

class Orkiv(App):
    def connect_to_jabber(self, jabber_id, password):
        self.xmpp = ClientXMPP(jabber_id, password)
        self.xmpp.connect()
        self.xmpp.process()
        self.xmpp.send_presence()
        self.xmpp.get_roster()

Orkiv().run()


 
 

 


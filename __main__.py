from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty  # at top of file
from sleekxmpp import ClientXMPP  # at the top of the file
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView  # At the top of the file
from kivy.uix.label import Label
from sleekxmpp.exceptions import XMPPError
from sleekxmpp.jid import InvalidJID
from kivy.uix.button import Button
 
class ConnectionModal(ModalView):
    def __init__(self, jabber_id, password):
        super(ConnectionModal, self).__init__(auto_dismiss=False,
            anchor_y="bottom")
        self.label = Label(text="Connecting to %s..." % jabber_id)
        self.add_widget(self.label)
        self.jabber_id = jabber_id
        self.password = password
        self.on_open = self.connect_to_jabber

    def connect_to_jabber(self):
        app = Orkiv.get_running_app()
        try:
            app.connect_to_jabber(self.jabber_id, self.password)
            self.label.text = "\n".join(app.xmpp.client_roster.keys())
        except (XMPPError, InvalidJID):
            self.label.text = "Sorry, couldn't connect, check your credentials"
            button = Button(text="Try Again")
            button.size_hint = (1.0, None)
            button.height = "40dp"
            button.bind(on_press=self.dismiss)
            self.add_widget(button)
            app.disconnect_xmpp()


class AccountDetailsTextInput(TextInput):
    next = ObjectProperty()
 
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 9:  # 9 is the keycode for 
            self.next.focus = True
        elif keycode[0] == 13:  # 13 is the keycode for 
            self.parent.parent.parent.login()  # this is not future friendly
        else:
            super(AccountDetailsTextInput, self)._keyboard_on_key_down(
                    window, keycode, text, modifiers)

class AccountDetailsForm(AnchorLayout):

    server_box = ObjectProperty()
    username_box = ObjectProperty()
    password_box = ObjectProperty()

    def login(self):
        jabber_id = self.username_box.text + "@" + self.server_box.text
        modal = ConnectionModal(jabber_id, self.password_box.text)
        modal.open()
     
class Orkiv(App):


    def __init__(self):
        super(Orkiv, self).__init__()
        self.xmpp = None

    def connect_to_jabber(self, jabber_id, password):
        self.xmpp = ClientXMPP(jabber_id, password)
        #~ self.xmpp.connect()

        self.xmpp.reconnect_max_attempts = 1
        connected = self.xmpp.connect()
        if not connected:
            raise XMPPError("unable to connect")

        self.xmpp.process()
        self.xmpp.send_presence()
        self.xmpp.get_roster()

    def disconnect_xmpp(self):
        if self.xmpp and self.xmpp.state.ensure("connected"):
            self.xmpp.abort()
        self.xmpp = None

    def on_stop(self):
        self.disconnect_xmpp()

Orkiv().run()


 
 

 


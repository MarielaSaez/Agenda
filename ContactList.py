import sqlite3
#comentario
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class ContactList(BoxLayout):
    def __init__(self, **kwargs):
        super(ContactList, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10

        self.contacts = []

        self.db_connection = sqlite3.connect("contacts.db")
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT
            )
        """)

        self.lbl_title = Label(text="Agenda de contactos")
        self.add_widget(self.lbl_title)

        self.lbl_name = Label(text="Nombre:")
        self.add_widget(self.lbl_name)
        self.txt_name = TextInput()
        self.add_widget(self.txt_name)

        self.lbl_phone = Label(text="Teléfono:")
        self.add_widget(self.lbl_phone)
        self.txt_phone = TextInput()
        self.add_widget(self.txt_phone)

        self.btn_add = Button(text="Agregar")
        self.btn_add.bind(on_press=self.add_contact)
        self.add_widget(self.btn_add)

        self.btn_refresh = Button(text="Actualizar lista")
        self.btn_refresh.bind(on_press=self.refresh_list)
        self.add_widget(self.btn_refresh)

        self.lbl_contacts = Label(text="Contactos:")
        self.add_widget(self.lbl_contacts)

        self.lst_contacts = BoxLayout(orientation="vertical")
        self.add_widget(self.lst_contacts)

        self.refresh_list()

    def add_contact(self, instance):
        name = self.txt_name.text.strip()
        phone = self.txt_phone.text.strip()

        if name and phone:
            self.db_cursor.execute("""
                INSERT INTO contacts (name, phone)
                VALUES (?, ?)
            """, (name, phone))
            self.db_connection.commit()

            self.txt_name.text = ""
            self.txt_phone.text = ""

            self.refresh_list()

    def refresh_list(self, *args):
        self.contacts = []
        self.lst_contacts.clear_widgets()

        self.db_cursor.execute("SELECT * FROM contacts")
        results = self.db_cursor.fetchall()

        for contact in results:
            self.contacts.append(contact)

            contact_widget = BoxLayout(orientation="horizontal")
            contact_widget.add_widget(Label(text=contact[1]))
            contact_widget.add_widget(Label(text=contact[2]))
            self.lst_contacts.add_widget(contact_widget)


class MyApp(App):
    def build(self):
        return ContactList()


if __name__ == '__main__':
    MyApp().run()

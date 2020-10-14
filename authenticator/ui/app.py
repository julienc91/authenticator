# -*- coding: utf-8 -*-

from typing import List

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen

import vault.interface
from ..vault import OTP, SessionMaker


class OTPWidget(RecycleDataViewBehavior, BoxLayout):
    code_label = StringProperty()
    id_label = StringProperty()
    progress = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.otp = None
        Clock.schedule_interval(self.update_progress, 0.1)

    def refresh_view_attrs(self, rv, index, data):
        self.otp = data["otp"]
        self.update_id_label()
        self.update_code()
        return super().refresh_view_attrs(rv, index, data)

    def update_id_label(self):
        issuer = self.otp.issuer
        label = self.otp.label
        if issuer and label:
            self.id_label = f"{issuer}:{label}"
        else:
            self.id_label = f"{issuer}{label}"

    def update_code(self, *_):
        if not self.otp:
            return

        code = self.otp.generate()
        digits = self.otp.digits
        code = f"{int(code):0{digits}}"
        self.code_label = code
        Clock.schedule_once(self.update_code, self.otp.get_next_change_timeout())

    def update_progress(self, *_):
        if not self.otp:
            return

        interval = self.otp.interval
        timeout = self.otp.get_next_change_timeout()
        self.progress = 100.0 * timeout / interval


class OTPList(RecycleView):

    search_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_data()

    def get_items(self) -> List[OTP]:
        session = SessionMaker()
        return vault.interface.get_all_otp(session, search=self.search_text)

    def set_search_text(self, value):
        self.search_text = value
        self.refresh_data()

    def refresh_data(self):
        self.data = [{"otp": otp} for otp in self.get_items()]


class OTPFilter(BoxLayout):
    pass


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class AuthenticatorApp(App):
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy import config
config.Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

import LRButton

Builder.load_string("""
<Example>:
    one: one
    AnchorLayout:
        anchor_x:'left'
        anchor_y:'top'
        GridLayout:
            cols: 2
            LRButton:
                text: "Text change when button is focused" if self.hovered else "This button is focused"
            LRButton:
                id: one
                text: "Different events for left and right button click"
""")

class Example(FloatLayout):

    def Left_Click(self, *args):
        self.one.text = "Left mouse button is pressed"

    def Right_Click(self, *args):
        self.one.text = "Right mouse button is pressed"




exa = Example()

class TestApp(App):


    def build(self):
        exa.one.bind(on_press=exa.Left_Click, on_right_press=exa.Right_Click)
        return exa

if __name__ == '__main__':
    TestApp().run()

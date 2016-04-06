'''
Button
======
'''

__all__ = ('LRButton', )
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import OptionProperty, StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_string("""
<LRButton>:
    state_image: self.background_down if self.hovered else (self.background_normal if self.state == 'normal' else self.background_down) 
    canvas:
        Color:
            rgba: self.background_color
        BorderImage:
            border: self.border
            pos: self.pos
            size: self.size
            source: self.disabled_image if self.disabled else self.state_image
        Color:
            rgba: self.disabled_color if self.disabled else self.color
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
""")

class LRButton(Label):
    '''Button class, see module documentation for more information.

    :Events:
        `on_press`
            Fired when the left button is pressed.
        `on_press_r`
            Fired when the Right button is pressed.
        `on_release`
            Fired when the button is released (i.e., the touch/click that
            pressed the button goes away).
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    '''

    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    state = OptionProperty('normal', options=('normal', 'down','down_r'))
    '''State of the button, must be one of 'normal' or 'down'.
    The state is 'down' only when the button is currently touched/clicked,
    otherwise 'normal'.

    :data:`state` is an :class:`~kivy.properties.OptionProperty`.
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color, in the format (r, g, b, a).

    .. versionadded:: 1.0.8

    :data:`background_color` is a :class:`~kivy.properties.ListProperty`,
    default to [1, 1, 1, 1].
    '''

    background_normal = StringProperty(
        'atlas://data/images/defaulttheme/button')
    '''Background image of the button used for default graphical representation,
    when the button is not pressed.

    .. versionadded:: 1.0.4

    :data:`background_normal` is an :class:`~kivy.properties.StringProperty`,
    default to 'atlas: data/images/defaulttheme/button'
    '''

    background_down = StringProperty(
        'atlas://data/images/defaulttheme/button_pressed')
    '''Background image of the button used for default graphical representation,
    when the button is pressed.

    .. versionadded:: 1.0.4

    :data:`background_down` is an :class:`~kivy.properties.StringProperty`,
    default to 'atlas://data/images/defaulttheme/button_pressed'
    '''

    border = ListProperty([16, 16, 16, 16])
    '''Border used for :class:`~kivy.graphics.vertex_instructions.BorderImage`
    graphics instruction, used itself for :data:`background_normal` and
    :data:`background_down`. Can be used when using custom background.

    It must be a list of 4 value: (top, right, bottom, left). Read the
    BorderImage instruction for more information about how to play with it.

    :data:`border` is a :class:`~kivy.properties.ListProperty`, default to (16,
    16, 16, 16)
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        self.register_event_type('on_press')
        self.register_event_type('on_right_press')
        self.register_event_type('on_release')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(LRButton, self).__init__(**kwargs)

    def _do_press(self):
        self.state = 'down'

    def _do_press_r(self):
        self.state = 'down_r'

    def _do_release(self):
        self.state = 'normal'

    def on_mouse_pos(self, *args):
        pos = args[1]
        inside = self.collide_point(*pos)
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_touch_down(self, touch):
        if 'button' in touch.profile:
            if super(LRButton, self).on_touch_down(touch):
                return True
            if not self.collide_point(touch.x, touch.y):
                return False
            if self in touch.ud:
                return False
            touch.grab(self)
            touch.ud[self] = True
            if touch.button == 'right':
                self._do_press_r()
                self.dispatch('on_right_press')
            else:
                self._do_press()
                self.dispatch('on_press')
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        if super(LRButton, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(LRButton, self).on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self._do_release()
        self.dispatch('on_release')
        return True

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_right_press(self):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass


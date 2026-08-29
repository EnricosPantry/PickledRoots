# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from dateutil.tz import *

mod = "mod4"
terminal = guess_terminal()

# CODE BELOW enables qtile clock to use LocalTime instead of UniversalTime
# code taken from https://github.com/qtile/qtile/issues/1170

class Clock(widget.Clock):
    def _get_time(self):
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        return (now + self.DELTA).strftime(self.format)

# hook copied from https://github.com/qtile/qtile/issues/1518 to size correctly popup floating windows
# @hook.subscribe.client_new
# def floating_size_hints(window):
#     hints = window.window.get_wm_normal_hints()
#     if hints and hints['max_width']:
#         window.floating = True

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "i", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "l", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "control"], "k", lazy.layout.normalize(), desc="Reset window size"),
    Key([mod, "control"], "i", lazy.layout.maximize(), desc="Maximize window"),
    Key([], "XF86Display", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen",),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Monad layout keys
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="launch rofi search"),
    Key([mod], "s", lazy.spawn("rofi -show drun"), desc="launch rofi search"),
    Key([mod], "a", lazy.spawn("rofi -show"), desc="launch rofi applications"),
    Key([mod], "p", lazy.spawn("flameshot gui"), desc="launch screenshot tool"),
    # FN Keys functions
    Key([], "XF86AudioMute", lazy.spawn("changeVolume --toggle-mute"), desc="mute volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("changeVolume --decrease 5"), desc="volume decrease 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("changeVolume --increase 5"), desc="volume increase 5%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("changeBrightness -dec 5"), desc="brightness decrease 5%"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("changeBrightness -inc 5"), desc="brightness increase 5%"),
]

# Old group lables, not being used anymore

#groups = [
#	Group("1", label=""),
#	Group("2", label=""),
#	Group("3", label=""),
#	Group("4", label=""),
#	Group("5", label=""),
#	Group("6", label=""),
#	Group("7", label=""),
#	Group("8", label=""),
#	Group("9", label=""),
#]

# New group lables currently being used

groups = [
    Group("1", label="1"),
    Group("2", label="2"),
    Group("3", label="3"),
    Group("4", label="4"),
    Group("5", label="5"),
    Group("6", label="6"),
    Group("7", label="7"),
    Group("8", label="8"),
    ]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(ratio=0.6, margin=5, border_focus='#ffb86c', border_normal='#6272a4'),
    # layout.Columns(margin=5, border_focus='#ffb86c', border_normal='#6272a4'),
    layout.Max(margin=5),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    layout.RatioTile(margin=5, border_width=2, border_focus='#ffb86c', border_normal='#6272a4'),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="cantarell bold",
    fontsize=14,
    padding=6,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
            widget.TextBox(
                fmt="",
                foreground='#50fa7b',
                padding=8,
                fontsize=20,
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
                ),
            widget.GroupBox(
                margin_y=5,
                highlight_method='line',
                highlight_color='#282a36',
                this_current_screen_border='#ffb86c',
                this_screen_border='#6272a4',
			    other_current_screen_border='#282a36',
			    other_screen_border='282a36',
			    active='#f8f8f2',
			    inactive='#6272a4',
		    ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.CurrentLayout(
                icon_first=True,
                foreground='#f8f8f2',
			    background='#282a36',
		    ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
                ),
            #Widget no longer in use 
            #widget.Prompt(
            #    prompt='Run:  ',
            #    foreground='#f8f8f2',
			#    background='#ffb86c',
		    #),
            widget.Spacer(
                length=12,
                ),
            widget.TaskList(
                border='#282a36',
                icon_size=20,
                fontsize=0
                ),
            widget.Spacer(
                length=bar.STRETCH,
            ),
            widget.CPU(
                format='Cpu: {load_percent:.0f}%',
                foreground='#ff79c6',
            ),
            widget.Memory(
                fmt='Mem: {}',
                foreground='#8be9fd',
                measure_mem='G',
                format='{MemUsed:.1f}/{MemTotal:.0f}{mm}',
            ), 
            widget.Net(
                format='Mbps:  {down:.1f}  {up:.1f}',
                prefix='M',
                foreground='#bd93f9',
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.Systray(
            ),
            widget.Spacer(
                length=6,
            ),
            widget.Volume(
                fmt='  {}',
			    foreground='#f8f8f2',
			    volume_up_command='changeVolume --increase 5',
			    volume_down_command='changeVolume --decrease 5',
			    mute_command='changeVolume --toggle-mute ',
		    ),
            widget.Backlight(
                fmt=' {}',
                backlight_name='intel_backlight',
                step=5,
			    foreground='#f8f8f2',
                change_command='changeBrightness -set {0}',	
		    ),
		    widget.Battery(
                update_interval=1,
                format='{char} {percent:2.0%}',
                charge_char=' ',
                not_charging_char=' ',
                discharge_char=' ',
                empty_char='',
                unknown_char=' ?',
                full_char='',
			    foreground='#f8f8f2',
                low_foreground='#ff5555',
			    low_percentage=0.2,
		        show_short_text=False,
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.Clock(
                format="%a %d/%m/%y - %H:%M",
                ### DATETIME CODES CAN BE FOUND AT BOTTOM OF PAGE https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
                foreground='#ffb86c',
            ),
            #widget.QuickExit(
            #   default_text='',
            #   countdown_format='{}',
            #   foreground='#f8f8f2',
            #   background='#6272a4',
            #),
            ],
            30,
	    background="#282a36",
        border_width=[0, 0, 0, 0],  # Draw top and bottom borders
        border_color="#6272a4", 
        opacity=0.9,
	    margin=0,     		# The padding between the bar and windows
                   ),
         ), 

   Screen(
       top=bar.Bar(
            [
                widget.TextBox(
                fmt="",
                foreground='#ff5555',
                padding=8,
                fontsize=20,
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
                ),
            widget.GroupBox(
                margin_y=5,
                highlight_method='line',
                highlight_color='#282a36',
                this_current_screen_border='#ffb86c',
                this_screen_border='#6272a4',
			    other_current_screen_border='#282a36',
			    other_screen_border='282a36',
			    active='#f8f8f2',
			    inactive='#6272a4',
		    ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.CurrentLayout(
                icon_first=True,
                foreground='#f8f8f2',
			    background='#282a36',
		    ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
                ),
            #Widget no longer in use 
            #widget.Prompt(
            #    prompt='Run:  ',
            #    foreground='#f8f8f2',
			#    background='#ffb86c',
		    #),
            widget.Spacer(
                length=12,
                ),
            widget.TaskList(
                border='#282a36',
                icon_size=20,
                fontsize=0
                ),
            widget.Spacer(
                length=bar.STRETCH,
            ),
            widget.CPU(
                format='Cpu: {load_percent:.0f}%',
                foreground='#ff79c6',
            ),
            widget.Memory(
                fmt='Mem: {}',
                foreground='#8be9fd',
                measure_mem='G',
                format='{MemUsed:.1f}/{MemTotal:.0f}{mm}',
            ), 
            widget.Net(
                format='Mbps:  {down:.1f}  {up:.1f}',
                prefix='M',
                foreground='#bd93f9',
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.Volume(
                fmt='  {}',
			    foreground='#f8f8f2',
			    volume_up_command='changeVolume --increase 5',
			    volume_down_command='changeVolume --decrease 5',
			    mute_command='changeVolume --toggle-mute ',
		    ),
            widget.Backlight(
                fmt=' {}',
                backlight_name='intel_backlight',
                step=5,
			    foreground='#f8f8f2',
                change_command='changeBrightness -set {0}',	
		    ),
		    widget.Battery(
                update_interval=1,
                format='{char} {percent:2.0%}',
                charge_char=' ',
                not_charging_char=' ', 
                discharge_char=' ',
                empty_char='',
                unknown_char=' ?',
                full_char='',
			    foreground='#f8f8f2',
                low_foreground='#ff5555',
			    low_percentage=0.2,
		        show_short_text=False,
            ),
            widget.Sep(
                foreground='#f8f8f2',
                linewidth=2,
            ),
            widget.Clock(
                format="%a %d/%m/%y - %H:%M",
                ### DATETIME CODES CAN BE FOUND AT BOTTOM OF PAGE https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
                foreground='#ffb86c',
            ),
            ],
            30,
            background="#282a36",
            border_width=[0, 0, 0, 0],  # Draw top and bottom borders
            border_color="#6272a4",
            opacity=0.9,
            margin=0, 			# The padding between bar and windows
                   ),
         ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

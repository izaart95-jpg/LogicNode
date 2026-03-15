# Linux Ricing & Window Managers

Ricing is the practice of customizing a Linux desktop's appearance and workflow to the extreme — theming, window managers, bars, compositors, fonts, and terminal aesthetics. The term comes from automotive "RICE" culture and is used affectionately in the Linux community.

---

## Table of Contents
1. [What is Ricing](#1-what-is-ricing)
2. [Window Manager Types](#2-window-manager-types)
3. [Hyprland](#3-hyprland)
4. [i3wm](#4-i3wm)
5. [bspwm](#5-bspwm)
6. [Awesome WM](#6-awesome-wm)
7. [niri](#7-niri)
8. [Other Notable WMs](#8-other-notable-wms)
9. [Compositors](#9-compositors)
10. [Status Bars](#10-status-bars)
11. [Theming Stack](#11-theming-stack)
12. [Dotfiles Management](#12-dotfiles-management)
13. [Community & Inspiration](#13-community--inspiration)

---

## 1. What is Ricing

```
A "rice" is a complete desktop customization setup covering:

  Window Manager:    How windows are placed and managed
  Compositor:       Visual effects (transparency, blur, animations)
  Status Bar:       System info display (clock, CPU, volume, workspaces)
  Terminal:         Alacritty, Kitty, Wezterm — configured with fonts + colors
  Shell Prompt:     Starship, Oh My Zsh, custom PS1
  Color Scheme:     Catppuccin, Dracula, Nord, Gruvbox, Tokyo Night, One Dark
  Font:             Nerd Fonts (patched with icons), JetBrains Mono, Iosevka
  File Manager:     lf, nnn, ranger (TUI) or Thunar, Nemo (GUI)
  App Launcher:     rofi, wofi, fuzzel, anyrun
  Notification Daemon: dunst, mako, swaync
  Wallpaper:        swww, feh, nitrogen, hyprpaper
  Lock Screen:      hyprlock, swaylock, i3lock-fancy
  Screenshot:       grim+slurp (Wayland), scrot, flameshot

Display protocols:
  X11 (Xorg):   Older, most compatible, most WMs support it
  Wayland:       Newer, better security, better HiDPI, the future
                 Native on: Hyprland, niri, sway, river
                 XWayland: compatibility layer for X11 apps under Wayland
```

### The Ricing Workflow

```
1. Choose base: usually Arch Linux (most ricer default), Void, Gentoo, NixOS
   (Ubuntu/Fedora work too but community leans Arch)
2. Install minimal base + window manager (no DE)
3. Write config files (dotfiles) for each component
4. Choose color scheme — apply consistently across all components
5. Share on r/unixporn with "Screenshot Saturday" or "Desktop thread"
```

---

## 2. Window Manager Types

```
Stacking (Floating):
  Windows overlap freely like Windows/macOS
  Examples: Openbox, Fluxbox, JWM
  Best for: traditional desktop feel with minimal DE

Tiling:
  Windows automatically arranged to fill screen — no overlapping
  Every window gets a portion of screen space
  Keyboard-driven: no mouse needed for window management
  Examples: i3, bspwm, awesome, dwm, qtile, herbstluftwm

Dynamic tiling:
  Combines tiling layouts with floating — switch between modes
  Examples: Hyprland, sway, qtile, awesome (with layouts)

Manual tiling:
  User places windows in a grid manually
  Examples: bspwm (binary space partition), herbstluftwm

Compositing WM:
  Built-in compositor + window manager combined
  Examples: KWin (KDE), Mutter (GNOME), Hyprland

Desktop Environments (DEs) — not WMs but relevant:
  GNOME, KDE Plasma, XFCE, LXQt — include WM + everything else
  Ricers usually skip DEs and use standalone WMs for full control
```

---

## 3. Hyprland

- **Website:** https://hyprland.org
- **Repository:** https://github.com/hyprwm/Hyprland
- **License:** BSD-3-Clause
- **Protocol:** Wayland only
- **Rendering:** GPU-accelerated (OpenGL/Vulkan), per-window animations
- **Status:** Most popular ricer WM as of 2024–2025

### Overview

Hyprland is a dynamic tiling Wayland compositor with smooth animations, rounded corners, blur effects, and highly configurable per-window rules — all out of the box. It's become the dominant choice in the ricing community because it looks impressive with minimal configuration while remaining keyboard-driven and efficient.

### Installation

```bash
# Arch Linux (AUR or official repos)
sudo pacman -S hyprland             # Official repos (stable)
yay -S hyprland-git                 # AUR (bleeding edge)

# Fedora
sudo dnf install hyprland

# Ubuntu/Debian — build from source or use third-party repo
# See: https://hyprland.org/getting_started/installation/

# NixOS (home-manager)
programs.hyprland.enable = true;
```

### Configuration (~/.config/hypr/hyprland.conf)

```ini
# ===== MONITORS =====
monitor=,preferred,auto,1          # Auto-detect monitor, native res, scale 1
monitor=DP-1,2560x1440@144,0x0,1   # Specific: DP-1, 1440p 144Hz, position, scale
monitor=eDP-1,1920x1080,auto,1     # Laptop screen

# ===== ENVIRONMENT VARIABLES =====
env = XCURSOR_SIZE,24
env = QT_QPA_PLATFORMTHEME,qt5ct
env = GDK_BACKEND,wayland,x11      # Prefer Wayland, fall back to X11

# ===== STARTUP PROGRAMS =====
exec-once = waybar                  # Status bar
exec-once = swww-daemon             # Wallpaper daemon
exec-once = dunst                   # Notification daemon
exec-once = nm-applet               # Network manager tray
exec-once = swww img ~/wallpaper.jpg

# ===== THEMING =====
general {
    gaps_in = 5                     # Gap between windows
    gaps_out = 10                   # Gap between windows and screen edge
    border_size = 2
    col.active_border = rgba(cba6f7ff) rgba(89b4faff) 45deg  # Gradient border
    col.inactive_border = rgba(595959aa)
    layout = dwindle                # dwindle (like i3) or master
    allow_tearing = false
}

decoration {
    rounding = 10                   # Rounded corners (pixels)
    blur {
        enabled = true
        size = 3                    # Blur radius
        passes = 1                  # Blur quality (more = slower)
        vibrancy = 0.1696
    }
    drop_shadow = true
    shadow_range = 4
    shadow_render_power = 3
    col.shadow = rgba(1a1a1aee)
}

animations {
    enabled = yes
    bezier = myBezier, 0.05, 0.9, 0.1, 1.05   # Custom easing curve
    animation = windows, 1, 7, myBezier         # Window open/close
    animation = windowsOut, 1, 7, default, popin 80%
    animation = border, 1, 10, default
    animation = fade, 1, 7, default
    animation = workspaces, 1, 6, default
}

# ===== INPUT =====
input {
    kb_layout = us
    kb_variant =
    follow_mouse = 1
    touchpad {
        natural_scroll = yes
        tap-to-click = yes
    }
    sensitivity = 0                 # -1.0 to 1.0 (0 = no adjustment)
}

# ===== LAYOUTS =====
dwindle {
    pseudotile = yes                # Windows maintain their size when tiled
    preserve_split = yes
}

master {
    new_is_master = true
}

# ===== KEYBINDINGS =====
$mainMod = SUPER                    # Windows/Super key

# Launch apps
bind = $mainMod, RETURN, exec, alacritty          # Terminal
bind = $mainMod, D, exec, wofi --show drun        # App launcher
bind = $mainMod, E, exec, thunar                  # File manager
bind = $mainMod, B, exec, firefox                 # Browser
bind = $mainMod SHIFT, S, exec, grim -g "$(slurp)" - | wl-copy  # Screenshot

# Window management
bind = $mainMod, Q, killactive                    # Close window
bind = $mainMod, F, fullscreen                    # Fullscreen
bind = $mainMod, V, togglefloating                # Float/tile toggle
bind = $mainMod, P, pseudo                        # Pseudotile

# Focus movement (vim keys)
bind = $mainMod, H, movefocus, l
bind = $mainMod, L, movefocus, r
bind = $mainMod, K, movefocus, u
bind = $mainMod, J, movefocus, d

# Move windows
bind = $mainMod SHIFT, H, movewindow, l
bind = $mainMod SHIFT, L, movewindow, r
bind = $mainMod SHIFT, K, movewindow, u
bind = $mainMod SHIFT, J, movewindow, d

# Resize windows
binde = $mainMod ALT, H, resizeactive, -20 0
binde = $mainMod ALT, L, resizeactive, 20 0
binde = $mainMod ALT, K, resizeactive, 0 -20
binde = $mainMod ALT, J, resizeactive, 0 20

# Workspaces (switch)
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
# ... up to 10

# Move window to workspace
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2

# Mouse binds
bindm = $mainMod, mouse:272, movewindow      # Drag to move
bindm = $mainMod, mouse:273, resizewindow    # Right-drag to resize

# Scroll through workspaces
bind = $mainMod, mouse_down, workspace, e+1
bind = $mainMod, mouse_up, workspace, e-1

# ===== WINDOW RULES =====
windowrulev2 = float, class:^(pavucontrol)$         # Float specific apps
windowrulev2 = float, title:^(Picture-in-Picture)$  # Float PiP
windowrulev2 = workspace 2, class:^(firefox)$       # Auto-assign to workspace
windowrulev2 = opacity 0.9 0.7, class:^(Alacritty)$ # 90% active / 70% inactive opacity
windowrulev2 = noshadow, floating:0                  # No shadow on tiled

# ===== WORKSPACES =====
workspace = 1, monitor:DP-1, default:true
workspace = 2, monitor:DP-1
workspace = 3, monitor:eDP-1
```

### Hyprland Ecosystem

```
hyprpaper:    Wallpaper manager for Hyprland (first-party)
hyprlock:     Lock screen (first-party)
hypridle:     Idle management — auto lock + suspend (first-party)
hyprshot:     Screenshot utility
xdg-desktop-portal-hyprland: Portal for screen sharing, file picker

Install ecosystem:
  sudo pacman -S hyprpaper hyprlock hypridle xdg-desktop-portal-hyprland
```

---

## 4. i3wm

- **Website:** https://i3wm.org
- **License:** BSD
- **Protocol:** X11
- **Style:** Manual tiling, tree-based layout

### Overview

i3 is the classic tiling WM — the entry point for most people into tiling WMs. Simple configuration, excellent documentation, stable and reliable. Everything is keyboard driven. sway is its Wayland equivalent (near-identical config).

### Installation

```bash
sudo apt install i3 i3blocks i3lock rofi           # Debian/Ubuntu
sudo pacman -S i3-wm i3blocks i3lock dmenu         # Arch
```

### Configuration (~/.config/i3/config)

```
# Modifier key (Super = Windows key, Mod1 = Alt)
set $mod Mod4

# Font for window titles
font pango:JetBrainsMono Nerd Font 10

# Terminal
bindsym $mod+Return exec alacritty

# App launcher
bindsym $mod+d exec rofi -show drun

# Kill window
bindsym $mod+Shift+q kill

# Window focus (vim keys)
bindsym $mod+h focus left
bindsym $mod+j focus down
bindsym $mod+k focus up
bindsym $mod+l focus right

# Move windows
bindsym $mod+Shift+h move left
bindsym $mod+Shift+j move down
bindsym $mod+Shift+k move up
bindsym $mod+Shift+l move right

# Split orientation
bindsym $mod+b split h       # Split horizontally
bindsym $mod+v split v       # Split vertically

# Fullscreen
bindsym $mod+f fullscreen toggle

# Layout switching
bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split

# Float toggle
bindsym $mod+Shift+space floating toggle

# Workspaces
set $ws1 "1"
set $ws2 "2: "
set $ws3 "3: "

bindsym $mod+1 workspace $ws1
bindsym $mod+Shift+1 move container to workspace $ws1

# Reload / restart / exit
bindsym $mod+Shift+c reload
bindsym $mod+Shift+r restart
bindsym $mod+Shift+e exec i3-nagbar -t warning -m 'Exit i3?' -B 'Yes' 'i3-msg exit'

# Resize mode
mode "resize" {
    bindsym h resize shrink width 10 px
    bindsym j resize grow height 10 px
    bindsym k resize shrink height 10 px
    bindsym l resize grow width 10 px
    bindsym Return mode "default"
    bindsym Escape mode "default"
}
bindsym $mod+r mode "resize"

# Borders and gaps (with i3-gaps)
gaps inner 8
gaps outer 4
default_border pixel 2

# Colors (Catppuccin Mocha)
set $base   #1e1e2e
set $mantle #181825
set $crust  #11111b
set $text   #cdd6f4
set $mauve  #cba6f7
set $blue   #89b4fa

client.focused          $mauve  $base   $text   $mauve  $mauve
client.focused_inactive $mantle $base   $text   $mantle $mantle
client.unfocused        $mantle $base   $text   $mantle $mantle

# Autostart
exec --no-startup-id picom --config ~/.config/picom/picom.conf
exec --no-startup-id polybar main
exec --no-startup-id feh --bg-fill ~/wallpaper.jpg
exec --no-startup-id dunst
```

### i3 Layout System

```
Containers in i3 form a tree:
  Workspace → split containers → windows

Types of container splits:
  h-split:   windows side by side
  v-split:   windows stacked
  stacking:  only one visible (like browser tabs)
  tabbed:    all visible with tabs at top

Create horizontal split:
  $mod+b then $mod+Return (open new terminal beside current)
  
Create vertical split:
  $mod+v then $mod+Return (open new terminal below current)

Move window to new workspace without following:
  $mod+Shift+[number] (window goes, focus stays)
  
Follow window to new workspace:
  $mod+[number] after moving (now follow it)

Scratchpad (hidden floating workspace):
  $mod+Shift+minus   (send window to scratchpad)
  $mod+minus         (show/hide scratchpad)
```

---

## 5. bspwm

- **Repository:** https://github.com/baskerville/bspwm
- **Companion:** sxhkd (Simple X Hotkey Daemon) — handles all keybindings
- **Protocol:** X11
- **Style:** Binary Space Partitioning tiling

### Overview

bspwm (Binary Space Partitioning Window Manager) uses a binary tree to manage windows. It has no built-in keybindings — sxhkd handles all shortcuts and sends commands to bspwm via `bspc`. This separation makes it extremely scriptable.

### Configuration

```bash
# ~/.config/bspwm/bspwmrc (executable shell script)

#!/bin/sh

# Start sxhkd (hotkey daemon)
pgrep -x sxhkd > /dev/null || sxhkd &

# Workspaces (desktops)
bspc monitor -d I II III IV V VI VII VIII IX X

# Window appearance
bspc config border_width         2
bspc config window_gap          10
bspc config focused_border_color "#cba6f7"  # Catppuccin Mauve
bspc config normal_border_color  "#313244"
bspc config presel_feedback_color "#89b4fa"

# Behavior
bspc config split_ratio          0.52
bspc config borderless_monocle   true
bspc config gapless_monocle      true
bspc config pointer_follows_focus false
bspc config focus_follows_pointer true

# Window rules
bspc rule -a Gimp state=floating
bspc rule -a firefox desktop='^2'
bspc rule -a Alacritty state=tiled

# Autostart
feh --bg-fill ~/wallpaper.jpg &
picom --config ~/.config/picom/picom.conf &
polybar main &
dunst &
```

```bash
# ~/.config/sxhkd/sxhkdrc (keybindings)

# Terminal
super + Return
    alacritty

# App launcher
super + d
    rofi -show drun

# Close/kill window
super + {_,shift + }w
    bspc node -{c,k}

# Focus/move windows (vim keys)
super + {h,j,k,l}
    bspc node -f {west,south,north,east}

super + shift + {h,j,k,l}
    bspc node -s {west,south,north,east}

# Rotate tree
super + r
    bspc node @/ -R 90

# Flip layout
super + {_,shift + }y
    bspc node @/ -F {horizontal,vertical}

# Tiled / pseudo_tiled / floating / fullscreen
super + {t,shift + t,f,shift + f}
    bspc node -t {tiled,pseudo_tiled,floating,fullscreen}

# Switch workspace
super + {1-9,0}
    bspc desktop -f '^{1-9,10}'

# Move window to workspace
super + shift + {1-9,0}
    bspc node -d '^{1-9,10}'

# Resize
super + alt + {h,j,k,l}
    bspc node -z {left -20 0,bottom 0 20,top 0 -20,right 20 0}

# Preselect split direction
super + ctrl + {h,j,k,l}
    bspc node -p {west,south,north,east}

# Cancel preselect
super + ctrl + space
    bspc node -p cancel

# Reload sxhkd
super + Escape
    pkill -USR1 -x sxhkd
```

---

## 6. Awesome WM

- **Website:** https://awesomewm.org
- **Repository:** https://github.com/awesomeWM/awesome
- **Language:** Configured in Lua
- **Protocol:** X11
- **Style:** Dynamic tiling — many built-in layouts

### Overview

Awesome WM is configured entirely in Lua — giving maximum flexibility at the cost of a steeper learning curve. It ships with a built-in status bar (Wibox), a notification library, and many tiling layouts. Popular in the ricing community because Lua lets you write complex logic (e.g., switch layout per workspace, custom widgets).

### Key Concepts

```lua
-- ~/.config/awesome/rc.lua

-- Load libraries
local awful = require("awful")
local wibox = require("wibox")
local beautiful = require("beautiful")
local naughty = require("naughty")

-- Theme (loads colors, fonts, icons)
beautiful.init(gears.filesystem.get_themes_dir() .. "default/theme.lua")

-- Modifier key
modkey = "Mod4"  -- Super key

-- Layouts available per workspace
awful.layout.layouts = {
    awful.layout.suit.tile,            -- Master + stack (like i3 default)
    awful.layout.suit.tile.left,       -- Master on left
    awful.layout.suit.tile.bottom,     -- Master on bottom
    awful.layout.suit.fair,            -- Equal-size grid
    awful.layout.suit.fair.horizontal,
    awful.layout.suit.spiral,          -- Fibonacci spiral
    awful.layout.suit.floating,        -- Free floating
    awful.layout.suit.magnifier,       -- Focus = fullscreen, others tiled around
    awful.layout.suit.max,             -- Only focused window shown
}

-- Key bindings
globalkeys = gears.table.join(
    -- Focus movement
    awful.key({ modkey }, "h", function() awful.client.focus.bydirection("left") end),
    awful.key({ modkey }, "l", function() awful.client.focus.bydirection("right") end),
    awful.key({ modkey }, "j", function() awful.client.focus.bydirection("down") end),
    awful.key({ modkey }, "k", function() awful.client.focus.bydirection("up") end),
    
    -- Switch workspace
    awful.key({ modkey }, "Left", awful.tag.viewprev),
    awful.key({ modkey }, "Right", awful.tag.viewnext),
    
    -- Change layout
    awful.key({ modkey }, "space", function() awful.layout.inc(1) end),
    
    -- Run launcher
    awful.key({ modkey }, "d", function() awful.spawn("rofi -show drun") end),
    
    -- Terminal
    awful.key({ modkey }, "Return", function() awful.spawn("alacritty") end),
    
    -- Resize master
    awful.key({ modkey }, ".", function() awful.tag.incmwfact(0.05) end),
    awful.key({ modkey }, ",", function() awful.tag.incmwfact(-0.05) end)
)

-- Wibox (status bar) widget example
local mytextclock = wibox.widget.textclock()
local mybattery = wibox.widget {
    widget = wibox.widget.textbox,
    text = "BAT: " .. battery_level()
}
```

---

## 7. niri

- **Repository:** https://github.com/YaLTeR/niri
- **License:** GPL v3
- **Protocol:** Wayland
- **Style:** Scrollable tiling (infinite horizontal workspace)

### Overview

niri is a fresh concept in window managers — a **scrollable tiling** Wayland compositor. Windows are arranged in columns that scroll horizontally. There are no workspaces in the traditional sense — you just scroll left and right through open windows. Inspired by PaperWM.

```
Traditional tiling (i3/bspwm):
  [Win1][Win2][Win3]  ← workspace 1
  [Win4][Win5]        ← workspace 2

niri (scrollable):
  ← ···[Win1][Win2][Win3][Win4][Win5]··· →
       scroll left/right to navigate
```

### Configuration (~/.config/niri/config.kdl)

```kdl
// KDL format (not TOML/YAML/JSON)

input {
    keyboard {
        xkb { layout "us" }
    }
    touchpad {
        tap
        natural-scroll
    }
}

output "eDP-1" {
    scale 1.0
    background-color "#1e1e2e"
}

layout {
    gaps 8
    center-focused-column "never"    // or "on-overflow"
    
    preset-column-widths {
        proportion 0.33333
        proportion 0.5
        proportion 0.66667
    }
    
    default-column-width { proportion 0.5; }
    
    focus-ring {
        width 2
        active-color "#cba6f7"
        inactive-color "#313244"
    }
    
    border {
        width 2
        active-color "#89b4fa"
        inactive-color "#45475a"
    }
}

animations {
    // Slowdown all animations:
    // slowdown 2.0
}

binds {
    // Modifier + key actions
    Mod+Return { spawn "alacritty"; }
    Mod+D { spawn "fuzzel"; }
    Mod+Q { close-window; }
    
    // Focus movement
    Mod+H { focus-column-left; }
    Mod+L { focus-column-right; }
    Mod+J { focus-window-down; }
    Mod+K { focus-window-up; }
    
    // Move windows
    Mod+Shift+H { move-column-left; }
    Mod+Shift+L { move-column-right; }
    Mod+Shift+J { move-window-down; }
    Mod+Shift+K { move-window-up; }
    
    // Resize
    Mod+R { switch-preset-column-width; }    // Cycle through preset widths
    Mod+Shift+R { reset-window-height; }
    Mod+F { maximize-column; }
    Mod+Shift+F { fullscreen-window; }
    
    // Workspaces (niri calls them workspaces too, but they scroll)
    Mod+1 { focus-workspace 1; }
    Mod+2 { focus-workspace 2; }
    Mod+Shift+1 { move-column-to-workspace 1; }
    
    // Screenshots
    Print { screenshot; }
    Shift+Print { screenshot-screen; }
}

// Window rules
window-rule {
    match app-id="pavucontrol"
    open-floating true
}
```

---

## 8. Other Notable WMs

### sway (Wayland i3)

```
Wayland compositor with near-identical config to i3
Drop-in i3 replacement for Wayland
Most i3 config works with minimal changes

Install: sudo pacman -S sway swaybar swaybg swayidle swaylock
Config:  ~/.config/sway/config (same syntax as i3, add Wayland-specific stuff)
```

### dwm (Dynamic Window Manager)

```
Suckless philosophy: < 2000 lines of C, configured by EDITING source code
No config file — change config.h, recompile, reinstall
Extremely minimal, no frills

Install: git clone https://git.suckless.org/dwm && cd dwm && make && sudo make install
Patches: https://dwm.suckless.org/patches/ (add features by patching C code)
```

### qtile (Python-configured)

```
Fully configured in Python — Wayland and X11 support
Great for people who know Python and want scripting power without Lua

Config: ~/.config/qtile/config.py
Install: sudo pacman -S qtile
```

### river (Wayland, Lua or shell)

```
Dynamic tiling Wayland compositor
External program (riverctl) controls everything — shell-scriptable
Config via shell scripts calling riverctl commands
```

### Openbox (Floating, X11)

```
Extremely lightweight floating WM
Most minimal X11 WM that still has good features
Config: XML (~/.config/openbox/rc.xml)
Often used as WM inside desktop environments (LXDE)
```

### herbstluftwm

```
Manual tiling WM controlled entirely via shell commands
Frames/splits done explicitly by user (not automatic like i3)
Powerful scripting since everything is a shell command
```

---

## 9. Compositors

A compositor handles visual effects: transparency, blur, shadows, animations.

### picom (X11)

```
The standard compositor for X11 WMs (i3, bspwm, awesome, Openbox)
Fork of compton, actively maintained

Install: sudo pacman -S picom

~/.config/picom/picom.conf:
backend = "glx";               # GPU-accelerated (vs "xrender")
vsync = true;
corner-radius = 8;             # Rounded corners
shadow = true;
shadow-radius = 7;
shadow-opacity = 0.7;
blur-method = "dual_kawase";   # Nice blur effect
blur-strength = 5;
fading = true;
fade-in-step = 0.03;
fade-out-step = 0.03;
# Transparency per window class:
opacity-rule = [
    "90:class_g = 'Alacritty'",
    "95:class_g = 'Rofi'"
];
# Launch: picom --config ~/.config/picom/picom.conf
```

### Hyprland (built-in)

```
Hyprland IS a compositor — no separate picom needed
Configure effects in hyprland.conf decoration block (see §3)
```

### swayfx (sway with effects)

```
Fork of sway adding blur, rounded corners, shadows
Same config as sway + additional effect options
```

---

## 10. Status Bars

### waybar (Wayland)

```
Most popular bar for Hyprland/sway
JSON config + CSS for styling

~/.config/waybar/config:
{
    "layer": "top",
    "position": "top",
    "height": 30,
    "spacing": 4,
    "modules-left": ["hyprland/workspaces", "hyprland/window"],
    "modules-center": ["clock"],
    "modules-right": ["pulseaudio", "network", "cpu", "memory", "battery", "tray"],
    
    "clock": {
        "format": " {:%H:%M}",
        "format-alt": " {:%A, %B %d, %Y}"
    },
    "cpu": { "format": " {usage}%" },
    "memory": { "format": " {}%" },
    "battery": {
        "states": { "warning": 30, "critical": 15 },
        "format": "{icon} {capacity}%",
        "format-icons": ["", "", "", "", ""]
    },
    "network": {
        "format-wifi": " {essid}",
        "format-ethernet": " {ifname}",
        "format-disconnected": "⚠ Disconnected"
    }
}

~/.config/waybar/style.css:
* { font-family: "JetBrainsMono Nerd Font"; font-size: 13px; }
window#waybar { background-color: rgba(30,30,46,0.9); color: #cdd6f4; }
#workspaces button.active { background-color: #cba6f7; color: #1e1e2e; }
```

### polybar (X11)

```
Highly customizable bar for X11 WMs
Module system with icons (requires Nerd Font)
Config: ~/.config/polybar/config.ini
```

### eww (Wayland + X11)

```
"Elkowl's Widgets" — build any widget/bar using Yuck (Lisp-like) + CSS
Maximum flexibility — create custom widgets, dashboards, popups
Steep learning curve: https://elkowar.github.io/eww/
```

---

## 11. Theming Stack

### Popular Color Schemes

```
Catppuccin:     Pastel, 4 flavors (Latte/Frappé/Macchiato/Mocha)
                https://github.com/catppuccin/catppuccin — ports for 500+ apps
Dracula:        Dark purple theme
                https://draculatheme.com — ports for 300+ apps
Nord:           Arctic, blue-toned
                https://nordtheme.com
Gruvbox:        Retro, warm earth tones
                https://github.com/morhetz/gruvbox
Tokyo Night:    Dark, blue-purple
                https://github.com/enkia/tokyo-night-vscode-theme
One Dark:       Based on Atom editor
Rosé Pine:      Pastel, pink-toned
Everforest:     Green, nature-inspired
```

### Terminal Emulators

```
Alacritty:   GPU-accelerated, minimal, fast. YAML/TOML config.
             https://alacritty.org
Kitty:       GPU-accelerated, more features (images, splits, protocols)
             https://sw.kovidgoyal.net/kitty/
Wezterm:     GPU-accelerated, Lua config, tabs/splits, multiplexer built-in
             https://wezfurlong.org/wezterm/
Foot:        Wayland-native, minimal, fast
             https://codeberg.org/dnkl/foot
```

### Fonts

```
Nerd Fonts:  Patched fonts with thousands of icons from icon sets
             https://nerdfonts.com
             Popular: JetBrainsMono Nerd Font, FiraCode Nerd Font,
                      Iosevka Nerd Font, Hack Nerd Font
             Install: sudo pacman -S ttf-jetbrains-mono-nerd

Install all Nerd Fonts (Arch):
  sudo pacman -S nerd-fonts

Icon libraries included in Nerd Fonts:
  Font Awesome, Material Design Icons, Devicons, Weather Icons, Powerline
```

### GTK Theming

```
GTK apps (Firefox, Thunar, GIMP, most Linux apps) use GTK theme:

~/.config/gtk-3.0/settings.ini:
[Settings]
gtk-theme-name = Catppuccin-Mocha-Standard-Mauve-Dark
gtk-icon-theme-name = Papirus-Dark
gtk-font-name = JetBrainsMono Nerd Font 11
gtk-cursor-theme-name = Catppuccin-Mocha-Dark-Cursors
gtk-cursor-theme-size = 24

Popular GTK themes:
  Catppuccin GTK:  https://github.com/catppuccin/gtk
  Dracula:         https://github.com/dracula/gtk
  Gruvbox:         https://github.com/TheGreatMcPain/gruvbox-material-gtk
  Orchis:          Clean material-inspired

nwg-look (Wayland GTK config GUI):
  sudo pacman -S nwg-look
```

---

## 12. Dotfiles Management

```
Dotfiles = all your config files (~/.config, ~/.bashrc, etc.)
Managed in a git repo so you can restore your setup on any machine.

Method 1: Bare git repo (most popular, no symlinks needed)
  git init --bare $HOME/.dotfiles
  alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
  dotfiles config --local status.showUntrackedFiles no
  
  # Use like git:
  dotfiles add ~/.config/hypr/hyprland.conf
  dotfiles commit -m "update hyprland config"
  dotfiles push
  
  # Restore on new machine:
  git clone --bare https://github.com/you/dotfiles $HOME/.dotfiles
  alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
  dotfiles checkout

Method 2: GNU Stow (symlink manager)
  Keep configs in ~/dotfiles/[package]/
  stow creates symlinks in $HOME
  
  ~/dotfiles/
    hypr/.config/hypr/hyprland.conf
    alacritty/.config/alacritty/alacritty.toml
    bash/.bashrc
  
  cd ~/dotfiles && stow hypr alacritty bash
  # Creates: ~/.config/hypr/hyprland.conf → ~/dotfiles/hypr/.config/hypr/hyprland.conf

Method 3: chezmoi (template-based)
  Handles sensitive data (encrypt secrets), cross-machine templates
  https://chezmoi.io
  
  chezmoi init
  chezmoi add ~/.config/hypr/hyprland.conf
  chezmoi apply
```

---

## 13. Community & Inspiration

```
r/unixporn:       https://reddit.com/r/unixporn — primary ricing showcase
                  Best resource: search "Hyprland" or "bspwm" for recent setups

r/UsabilityPorn:  Workflow-focused customization

GitHub topics:
  github.com/topics/dotfiles     → browse community dotfiles
  github.com/topics/hyprland     → Hyprland configs
  github.com/topics/rice         → full rices

Discord servers:
  Hyprland:  discord.gg/hyprland
  Linux Ricing communities

Notable dotfile repos to study:
  Search: "dotfiles" + your WM of choice
  Common showcase: github.com/[username]/dotfiles
```

---

## See Also

- [Linux Distributions](linux-distributions.md) — Arch is the ricer default; see also Void, NixOS
- [Desktop Environments](../mobile/desktop-environments.md) — Full DEs vs standalone WMs
- [Terminal Tools](../devtools/terminal-tools.md) — Tmux, terminal multiplexing
- [Linux Internals](linux-internals.md) — Wayland/X11 at the kernel and compositor level

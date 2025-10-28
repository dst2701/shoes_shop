"""
UI Enhancement Utilities - Button hover effects and animations
"""
import tkinter as tk

def add_button_hover_effect(button, original_bg, hover_bg, original_fg='white', hover_fg='white',
                            lift_amount=2, scale=1.02):
    """
    Add modern hover effects to a button

    Args:
        button: The tkinter button widget
        original_bg: Original background color
        hover_bg: Background color on hover
        original_fg: Original foreground (text) color
        hover_fg: Foreground color on hover
        lift_amount: Pixels to lift button on hover
        scale: Scale factor for button on hover (slight zoom effect)
    """
    original_cursor = button['cursor'] if 'cursor' in button.keys() else 'arrow'
    original_relief = button['relief'] if 'relief' in button.keys() else 'flat'

    def on_enter(e):
        """Handle mouse enter event - NO border change to prevent size shift"""
        button.config(
            bg=hover_bg,
            fg=hover_fg,
            relief='raised',
            cursor='hand2'
        )

    def on_leave(e):
        """Handle mouse leave event"""
        button.config(
            bg=original_bg,
            fg=original_fg,
            relief=original_relief,
            cursor=original_cursor
        )

    # Bind events
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def add_pulse_effect(button, color1, color2, interval=500):
    """
    Add a subtle pulsing effect to important buttons

    Args:
        button: The tkinter button widget
        color1: First color
        color2: Second color
        interval: Milliseconds between color changes
    """
    current_color = [0]  # Use list to maintain state
    colors = [color1, color2]

    def pulse():
        if button.winfo_exists():
            try:
                button.config(bg=colors[current_color[0]])
                current_color[0] = 1 - current_color[0]  # Toggle between 0 and 1
                button.after(interval, pulse)
            except:
                pass

    # Don't auto-start pulse, let caller decide
    return pulse


def add_click_effect(button):
    """
    Add a brief visual feedback when button is clicked
    """
    original_relief = button['relief']

    def on_click(e):
        """Handle button click animation"""
        button.config(relief='sunken')
        button.after(100, lambda: button.config(relief=original_relief))

    button.bind("<Button-1>", on_click)


def create_modern_button(parent, text, command, bg_color, fg_color='white',
                        font=('Arial', 12, 'bold'), padx=20, pady=10,
                        hover_color=None, **kwargs):
    """
    Create a modern-looking button with automatic hover effects

    Args:
        parent: Parent widget
        text: Button text
        command: Command to execute on click
        bg_color: Background color
        fg_color: Foreground (text) color
        font: Font tuple
        padx, pady: Padding
        hover_color: Color on hover (auto-generated if None)
        **kwargs: Additional button configuration

    Returns:
        The created button widget
    """
    # Auto-generate hover color if not provided (slightly lighter)
    if hover_color is None:
        hover_color = lighten_color(bg_color, 20)

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        font=font,
        padx=padx,
        pady=pady,
        relief='raised',
        bd=2,
        cursor='hand2',
        activebackground=hover_color,
        activeforeground=fg_color,
        **kwargs
    )

    # Add hover effects
    add_button_hover_effect(button, bg_color, hover_color, fg_color, fg_color)
    add_click_effect(button)

    return button


def lighten_color(color, percent):
    """
    Lighten a hex color by a percentage

    Args:
        color: Hex color string (e.g., '#3498db')
        percent: Percentage to lighten (0-100)

    Returns:
        Lightened hex color string
    """
    # Remove # if present
    color = color.lstrip('#')

    # Convert to RGB
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    # Lighten
    r = min(255, int(r + (255 - r) * percent / 100))
    g = min(255, int(g + (255 - g) * percent / 100))
    b = min(255, int(b + (255 - b) * percent / 100))

    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'


def darken_color(color, percent):
    """
    Darken a hex color by a percentage

    Args:
        color: Hex color string (e.g., '#3498db')
        percent: Percentage to darken (0-100)

    Returns:
        Darkened hex color string
    """
    # Remove # if present
    color = color.lstrip('#')

    # Convert to RGB
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    # Darken
    r = max(0, int(r * (1 - percent / 100)))
    g = max(0, int(g * (1 - percent / 100)))
    b = max(0, int(b * (1 - percent / 100)))

    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'


def add_smooth_scroll_effect(canvas):
    """
    Add smooth scrolling effect to canvas
    """
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    return _on_mousewheel


def add_entry_focus_effect(entry, focus_color='#3498db', normal_color='#bdc3c7'):
    """
    Add focus effect to entry fields
    """
    def on_focus_in(e):
        entry.config(highlightbackground=focus_color, highlightcolor=focus_color, highlightthickness=2)

    def on_focus_out(e):
        entry.config(highlightbackground=normal_color, highlightcolor=normal_color, highlightthickness=1)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# Color palette for consistent UI
COLORS = {
    'primary': '#3498db',      # Blue
    'success': '#27ae60',      # Green
    'danger': '#e74c3c',       # Red
    'warning': '#f39c12',      # Orange
    'info': '#9b59b6',         # Purple
    'dark': '#2c3e50',         # Dark Blue
    'light': '#ecf0f1',        # Light Gray
    'secondary': '#95a5a6',    # Gray
}


def get_hover_color(base_color):
    """Get appropriate hover color for a base color"""
    color_map = {
        '#3498db': '#5dade2',  # Primary blue -> lighter
        '#27ae60': '#2ecc71',  # Success green -> lighter
        '#e74c3c': '#ec7063',  # Danger red -> lighter
        '#f39c12': '#f8c471',  # Warning orange -> lighter
        '#9b59b6': '#af7ac5',  # Info purple -> lighter
        '#2c3e50': '#34495e',  # Dark -> lighter
        '#95a5a6': '#aab7b8',  # Secondary -> lighter
    }

    return color_map.get(base_color, lighten_color(base_color, 15))


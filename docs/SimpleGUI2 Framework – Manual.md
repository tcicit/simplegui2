# SimpleGUI2 Framework – Manual

## 1. Idea and Intention

**SimpleGUI2** was developed to simplify and accelerate the creation of graphical user interfaces (GUIs) in Python. The goal is to strictly separate layout and logic: The layout is described declaratively in YAML files, while the logic remains in Python. This allows for quick adjustments to interfaces without changing Python code. The framework supports standard Tkinter widgets, ttk widgets, and custom extensions.

---

## 2. Explanation of the Framework and Architecture

### Core Principles

- **Separation of Layout and Logic:** Layout in YAML, logic in Python.
- **Rapid Prototyping:** GUI changes without Python code.
- **Reusability:** Layouts can be used as templates.
- **Declarative Layout:** The GUI structure is defined in YAML files as a tree of rows (`rows`) and columns (`columns`).
- **Logic in Python:** Python functions are linked to `command` strings referenced in YAML via a mapping mechanism (`command_mapping`).
- **Theming:** A central theme object controls colors, fonts, etc., for a consistent look and feel.
- **Extensibility:** Custom widgets and themes are easily possible.

### Architecture Overview

- **core.py:** Contains the central class `SimpleGUI`, which builds the layout and provides methods for widget interaction.
- **layout_manager.py:** Loads the YAML layout, maps commands, and builds the menu.
- **core_functions.py & core_demo_app_functions.py:** Contain the logic for standard and app-specific commands.
- **theme_manager.py:** Central theming for all widgets.
- **custom_widgets.py:** Custom widgets like Card, InfoBox, Picture, ColorPicker.
- **yaml_loader.py:** Loads and parses YAML layouts.
- **validation.py:** Validates layout and inputs.
- **filedialogs.py:** Encapsulates file and directory selection dialogs.

---

## Prerequisites and Installation

### Prerequisites

- **Python 3.8 or newer**
  The framework is based on Python 3 and uses standard libraries like `tkinter` as well as optional packages for extended widgets.
- **Tkinter**
  Tkinter is included in most Python distributions. On Linux, it might need to be installed separately (see below).

### Installation

1.  **Download or clone the repository**

```sh
    git clone <REPOSITORY-URL>
    cd simpleGUI2
```

2.  **Install dependencies**

   For basic functionality, Python with Tkinter is usually sufficient.
   For optional features (e.g., Markdown/HTML preview), additional packages may be necessary:

```sh
        pip install pyyaml
```

   For Markdown/HTML preview, possibly:

```sh
     pip install markdown
```

3.  **Install Tkinter on Linux (if not present)**

```sh
    sudo apt-get install python3-tk
```

4.  **Start the example application**

```sh
    python3 core_demo_app.py
```

### Notes

- The framework is cross-platform (Windows, Linux, macOS).
- For your own projects, it is sufficient to copy the `simplegui` directory into your project or include it as a Python package.
- The YAML layouts and example scripts serve as templates for your own applications.

## 3. List of Widgets with Attributes

### Standard Widgets (tk)

| Type        | Attributes (Examples)        | Description                      |
|-------------|------------------------------|----------------------------------|
| Label       | text, bg, fg, font           | Text display                     |
| Entry       | width, show, textvariable   | Single-line input field          |
| Button      | text, command, state         | Button                           |
| Checkbutton | text, variable, value        | Checkbox                         |
| Radiobutton | text, value, variable        | Radio button                     |
| Text        | width, height, wrap, state   | Multi-line text field            |
| Frame       | bg, relief, bd               | Container for other widgets      |
| LabelFrame  | text, labelanchor, bg, fg    | Frame with a title               |
| Scale       | from_, to, orient, value     | Slider                           |
| Spinbox     | from_, to, increment, values | Number field with arrows         |
| Listbox     | height, width, selectmode    | List of selectable items         |
| Canvas      | width, height, bg            | Drawing area                     |

### Themed Widgets (ttk)

| Type        | Attributes (Examples)        | Description                      |
|-------------|------------------------------|----------------------------------|
| Combobox    | values, state, text          | Dropdown selection field         |
| Separator   | orient                       | Separator line                   |
| Notebook    | tabs                         | Tabbed container                 |
| Treeview    | columns, headings, show      | Table/Tree view                  |

### Custom Widgets

| Type            | Attributes (Examples)            | Description                          |
|-----------------|----------------------------------|--------------------------------------|
| Card            | title, content                   | Info card with title and content     |
| InfoBox         | message, info_type               | Info/Warning/Error message           |
| Picture         | filepath, width, height          | Image display                        |
| ColorPicker     | initial_color, button_text, show_hex, command | Color picker with preview            |
| HtmlPreviewArea | -                                | HTML preview (Markdown editor)       |

---

## 4. Application Examples

### YAML Layout with Rows and Columns (Excerpt)

```yaml
rows:
  - columns:
      - type: Label
        options: { text: "Username:" }
      - type: Entry
        name: username_entry
        options: { width: 30 }
  - columns:
      - type: Button
        name: ok_button
        options: { text: "OK" }
        command: "handle_ok"
```

### Python Code

```python
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout

def handle_ok(app):
    username = app.get_widget_value("username_entry")
    print(f"Username: {username}")

commands = { "handle_ok": handle_ok }
root = tk.Tk()
app = SimpleGUI(root, title="Demo", size="400x200")
setup_layout(app, "layout.yaml", commands)
app.run()
```

---

### YAML Layout with Grid (Excerpt)

```yaml
grid:
  - row: 0
    column: 0
    type: Label
    options:
      text: "First Name:"
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options:
      width: 20
  - row: 1
    column: 0
    type: Label
    options:
      text: "Last Name:"
  - row: 1
    column: 1
    type: Entry
    name: lastname_entry
    options:
      width: 20
  - row: 2
    column: 0
    type: Button
    options:
      text: "OK"
      command: "show_name"
    grid_options: # Corrected indentation for columnspan
      columnspan: 2
```

### Python Code

```python
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout

def show_name(app):
    firstname = app.get_widget_value("firstname_entry")
    lastname = app.get_widget_value("lastname_entry")
    print(f"Name: {firstname} {lastname}")

commands = { "show_name": show_name }
root = tk.Tk()
app = SimpleGUI(root, title="Grid Demo", size="400x200")
setup_layout(app, "grid_layout.yaml", commands)
app.run()
```

---

## 5. List of Messages and File Dialogs

The SimpleGUI2 framework provides convenient tools for user interaction with the `Messages` class and the `FileDialogs` module:

- **Messages**: Allow displaying informational, warning, and error messages, as well as dialogs for user queries (e.g., Yes/No, OK/Cancel).
- **FileDialogs**: Offer simple methods to select, save files or directories, or select multiple files – all with native system dialogs.

These functions facilitate user interaction and are indispensable in any GUI application.

#### Example: Using Messages and File Dialogs

```python
from simplegui.messages import Messages
from simplegui.filedialogs import FileDialogs

def open_and_show_file(app):
    filename = FileDialogs.open_file(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename:
        Messages.info("File Opened", f"You have selected the file:\n{filename}")
    else:
        Messages.warning("Cancelled", "No file was selected.")

def ask_user(app):
    if Messages.yesno("Question", "Do you want to continue?"):
        Messages.info("Continue", "You chose Yes.")
    else:
        Messages.error("Cancelled", "You chose No.")
```

**Note:**
All methods can be called directly and do not require their own window handling – the framework takes care of this automatically.

### Messages (simplegui/messages.py)

| Method                 | Description                                         | Return Value                      |
|------------------------|-----------------------------------------------------|-----------------------------------|
| info(title, msg)       | Displays an info messagebox                         | None                              |
| warning(title, msg)    | Displays a warning messagebox                       | None                              |
| error(title, msg)      | Displays an error messagebox                        | None                              |
| question(title, msg)   | Displays a question dialog ("Yes"/"No" as string)   | "yes" or "no"                     |
| yesno(title, msg)      | Displays a Yes/No dialog                            | True (Yes) / False (No)           |
| okcancel(title, msg)   | Displays an OK/Cancel dialog                        | True (OK) / False (Cancel)        |
| retrycancel(title, msg)| Displays a Retry/Cancel dialog                      | True (Retry) / False (Cancel)     |
| yesnocancel(title, msg)| Displays a Yes/No/Cancel dialog                     | True (Yes) / False (No) / None (Cancel) |

### File Dialogs (simplegui/filedialogs.py)

| Method                          | Description                                       |
|---------------------------------|---------------------------------------------------|
| open_file(...)                  | Open file                                         |
| save_file(...)                  | Save file                                         |
| open_directory(...)             | Select directory                                  |
| save_file_as(...)               | "Save as..."                                      |
| open_multiple_files(...)        | Select multiple files                             |
| open_file_with_title(...)       | Open file with title                              |
| save_file_with_title(...)       | Save file with title                              |
| open_directory_with_title(...)  | Select directory with title                       |
| ...                             | (Many other variants with initialdir, parent etc.)|

**All FileDialog methods return the selected path (or a list of paths).**

---

## 6. YAML Layout Reference

### Basic Structure

```yaml
rows:
  - columns:
      - type: Label
        options: { text: "Example" }
      - type: Entry
        name: input_field
        options: { width: 20 }
  - columns:
      - type: Button
        options: { text: "OK" }
        command: "handle_ok"
```

**Important Fields:**
- `type`: Widget type (see Widget List)
- `name`: Unique name for Python access (optional, recommended)
- `options`: Widget-specific options (e.g., `text`, `values`, `from_`, `to`)
- `pack_options` / `grid_options`: Control placement (e.g., `side`, `fill`, `expand`, `sticky`, `columnspan`)
- `command`: Name of the Python function (as a string) to be called

### Grid Layout

```yaml
grid:
  - row: 0
    column: 0
    type: Label
    options: { text: "First Name:" }
    grid_options: { sticky: w }
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options: { width: 20 }
    grid_options: { sticky: ew }
  # ...
```

**Additional Fields:**
- `parent`: Name of the parent widget (for nested layouts)
- `columnspan`, `rowspan`: Widget spans multiple columns/rows

- **rowspan**
  Specifies how many rows the widget should span.
  *Example:* `rowspan: 7` → The widget occupies 7 rows.

- **sticky**
  Determines which sides of the cell area the widget "sticks" to.
  *Possible values:*
  - `n` (north/top),
  - `s` (south/bottom),
  - `e` (east/right),
  - `w` (west/left),
  - combinations like `nsew` (fills the cell completely), `ew` (fills horizontally), `new` (north, east, west).

- **pady**
  Adds vertical external padding above and below the widget.
  *Example:* `pady: 5` → 5 pixels of padding top and bottom.

- **padx**
  Adds horizontal external padding to the left and right of the widget.
  *Example:* `padx: 10` → 10 pixels of padding left and right.

These options control the layout of widgets in Tkinter's grid manager.

---

### Grid Weights (row_weight, column_weight)
With grid weights (row_weight and column_weight), you determine how rows and columns adjust when the window is resized.
A higher weight means the corresponding row or column receives more space.

Usage in YAML layout:

```yaml
grid:
  - row: 0
    column: 0
    type: Label
    options: { text: "First Name:" }
  - row: 0
    column: 1
    type: Entry
    name: firstname_entry
    options: { width: 20 }
  - row: 1
    column: 0
    type: Label
    options: { text: "Last Name:" }
  - row: 1
    column: 1
    type: Entry
    name: lastname_entry
    options: { width: 20 }
  - row: 2
    column: 0
    type: Button
    options: { text: "OK", command: "show_name" }
    grid_options: { columnspan: 2 }

# Grid weights for flexible resizing
row_weights:
  0: 1
  1: 1
  2: 0
column_weights:
  0: 0
  1: 1
```

### Explanation:

- `row_weights` and `column_weights` are dictionaries that specify the weight for each row/column.
- In the example, the second column (column 1) expands when the window is widened.
- Rows 0 and 1 grow vertically, while row 2 (with the button) remains fixed.

**Note:**

Support for `row_weights` and `column_weights` must be present in the framework (e.g., by calling `grid_rowconfigure` and `grid_columnconfigure` in the code).

```python
import tkinter as tk
from simplegui.core import SimpleGUI
from simplegui.layout_manager import setup_layout

def show_name(app):
    firstname = app.get_widget_value("firstname_entry")
    lastname = app.get_widget_value("lastname_entry")
    print(f"Name: {firstname} {lastname}")

commands = { "show_name": show_name }
root = tk.Tk()
app = SimpleGUI(root, title="Grid with Weights", size="400x200")
setup_layout(app, "grid_with_weights.yaml", commands)
app.run()
```

**Tip:**
With grid weights, you can achieve flexible, responsive layouts – especially useful for professional interfaces!

---

## 7. Menu System

### YAML Example

```yaml
menu:
  - label: "File"
    items:
      - label: "Open"
        command: open_file
      - label: "Exit"
        command: exit_app
  - label: "Help"
    items:
      - label: "About"
        command: show_about
```

**Note:**
Each menu item can be linked to a Python function (`command`).

---

## 8. Validation and Error Handling

The framework provides validation functions for inputs and layouts:

- **Input Validation:**
  Using the `Validator` class (`simplegui/validation.py`), fields can be checked for "not empty", regex patterns, etc.

- **Layout Validation:**
  Loading and parsing YAML files automatically checks for errors and provides helpful error messages.

**Example:**

```python
from simplegui.validation import Validator

if not Validator.is_not_empty(app.get_widget_value("username_entry")):
    Messages.warning("Input Error", "Please enter a username.")
```

---

## 9. Theming and Customization

The appearance of the application can be centrally customized via the `ThemeManager`:

- Colors, fonts, and styles are defined in `simplegui/theme_manager.py`.
- Custom themes can be created by deriving and overriding the theme definition.

**Example:**

```python
from simplegui.theme_manager import ThemeManager

ThemeManager.set_theme("dark")  # Example for theme switching
```

---

## 10. Custom Widgets and Extensions

Custom widgets can be added by deriving from Tkinter or ttk widgets and integrating them into `custom_widgets.py`.
Mapping is done via the `_resolve_widget_class` method in `SimpleGUI`.

**Example:**

```python
class MyWidget(ttk.Frame):
    # Custom logic
    pass
```

---

## 11. FAQ / Troubleshooting

**Common Issues:**

- **Tkinter missing:**
  → Install with `sudo apt-get install python3-tk`
- **YAML errors:**
  → Check indentations and syntax, use a YAML validator.
- **Widgets not appearing:**
  → Check `name` and `parent` specifications as well as the layout structure.
- **Command not executing:**
  → Is the function name correct in the Python code and included in the mapping?

---

## 12. API Reference (Brief Overview)

- **SimpleGUI**
  - `build(layout)`: Builds the layout
  - `get_widget(name)`: Returns the widget object
  - `get_widget_value(name)`: Returns the value of an input widget
  - `set_widget_option(name, option, value)`: Sets a widget option

- **Messages**
  - `info`, `warning`, `error`, `yesno`, `okcancel`, `retrycancel`, `yesnocancel`, `question`

- **FileDialogs**
  - `open_file`, `save_file`, `open_directory`, `save_file_as`, ...

---

## 13. License and Contributing

- **License:**
  The framework is under an open-source license (see repository).
- **Contributing:**
  Contributions, bug reports, and feature requests are welcome!
  Repository: `<REPOSITORY-URL>`

---

## 14. Changelog

- **v1.0 (2025-05):**
  First stable version, YAML layout, theming, custom widgets, menu system, validation, examples.

---

*Further details and examples can be found in the source code and YAML layouts within the project.*
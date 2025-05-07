# SimpleGUI2

**SimpleGUI2** is a flexible Python framework for rapid GUI development using Tkinter and YAML. Layouts are described declaratively in YAML files, while logic stays in Python. The framework supports standard Tkinter widgets, ttk widgets, and custom extensions.

---

## Features

- **Declarative Layouts:** Define your GUI structure in YAML, keep logic in Python
- **Rich Widget Support:** Label, Entry, Button, Checkbutton, Radiobutton, Combobox, Treeview, Canvas, and more
- **Tabbed Interfaces:** Easily create tabbed UIs (Notebook)
- **Custom Widgets:** Card, InfoBox, Picture, ColorPicker, HtmlPreviewArea
- **Theming:** Central color scheme and fonts
- **Easy Extensibility:** Add your own widgets and themes

---

## Requirements

- **Python 3.8 or newer**
- **Tkinter** (usually included; on Linux: `sudo apt-get install python3-tk`)
- **PyYAML** (`pip install pyyaml`)
- **Pillow** (optional, for image support: `pip install pillow`)
- **Markdown** (optional, for Markdown/HTML preview: `pip install markdown`)

---

## Installation

1. **Clone the repository**
    ```sh
    git clone <REPOSITORY-URL>
    cd simpleGUI2
    ```

2. **Install dependencies**
    ```sh
    pip install pyyaml pillow markdown
    ```

---

## Quick Start

1. **Create a YAML layout** (e.g. `layout.yaml`)
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

2. **Write your Python code**
    ```python
    import tkinter as tk
    from simplegui.core import SimpleGUI
    from simplegui.yaml_loader import load_yaml_layout

    def handle_ok(app):
        username = app.get_widget_value("username_entry")
        print(f"Username: {username}")

    command_mapping = { "handle_ok": handle_ok }
    layout = load_yaml_layout("layout.yaml")

    # Map commands in the layout
    def map_layout_commands(layout_data, mapping):
        if isinstance(layout_data, dict):
            for key, value in layout_data.items():
                if key == "command" and isinstance(value, str) and value in mapping:
                    layout_data[key] = mapping[value]
                elif isinstance(value, (dict, list)):
                    map_layout_commands(value, mapping)
        elif isinstance(layout_data, list):
            for item in layout_data:
                map_layout_commands(item, mapping)
    map_layout_commands(layout, command_mapping)

    root = tk.Tk()
    app = SimpleGUI(root, title="Minimal Example", size="300x120")
    app.build(layout)
    app.run()
    ```

3. **Run your app**
    ```sh
    python demo_app_yaml.py
    ```

---

## Documentation

- Full manual: [docs/HANDBUCH.md](docs/HANDBUCH.md) (German)
- Example layouts: see `core_demo_app_layout.yaml`, `editor_demo_app_layout.yaml`, `markdown_demo/`
- More examples and details in the source code and YAML files

---

## License & Contributing

- **License:** Open Source (see LICENSE)
- **Contributions:** Issues, feature requests, and pull requests are welcome!  
  Repository: `<REPOSITORY-URL>`

---

*Last updated: 2025-05-07*
# /home/tci/Dokumente/Entwicklung/Python/simpleGUI2/tests/test_simplegui_build.py

import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch, MagicMock, ANY

# Adjust import paths based on your project structure
# If running from the root 'simpleGUI2' directory:
from simplegui.core import SimpleGUI
from simplegui.custom_widgets import Picture, Card, InfoBox
# We need yaml_loader to load the structure, or we simulate it
from simplegui.yaml_loader import load_yaml_layout

# --- Mock Pillow for tests ---
# Mock the PIL module IF it's not installed or to avoid file dependency
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Create mock objects that mimic PIL enough for the Picture widget
mock_image = MagicMock(spec=Image.Image)
mock_image.size = (100, 100) # Example size
mock_image.resize.return_value = mock_image # resize returns the mock itself
mock_photo_image = MagicMock(spec=ImageTk.PhotoImage)

# Use patch to replace PIL imports within the custom_widgets module during tests
# Patch 'Image.open' to return our mock image
# Patch 'ImageTk.PhotoImage' to return our mock photo image
# Patch 'PIL_AVAILABLE' flag if necessary
pil_open_patch = patch('simplegui.custom_widgets.Image.open', return_value=mock_image)
pil_photoimage_patch = patch('simplegui.custom_widgets.ImageTk.PhotoImage', return_value=mock_photo_image)
pil_available_patch = patch('simplegui.custom_widgets.PIL_AVAILABLE', True) # Assume available for most tests

# --- Test Class ---

class TestSimpleGUIBuildEnhanced(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the layout once for all tests in this class."""
        try:
            # Load the actual YAML file to test its structure
            cls.layout_data = load_yaml_layout("layout_enhanced.yaml")
            # Create dummy command functions for mapping
            cls.mock_commands = {
                "register_user": MagicMock(),
                "login_user": MagicMock(),
                "show_all_values": MagicMock(),
                "populate_treeview": MagicMock(),
                "clear_treeview_cmd": MagicMock(),
                "show_tree_selection": MagicMock(),
                "change_label": MagicMock(),
                "exit_app": MagicMock(),
                # Add any other commands from menu.yaml if needed for other tests
                "open_file": MagicMock(),
                "save_file": MagicMock(),
                "save_file_as": MagicMock(),
                "open_directory": MagicMock(),
                "copy_text": MagicMock(),
                "paste_text": MagicMock(),
                "about": MagicMock(),
            }
            # Simulate the command mapping step done in demo_app_yaml.py
            cls.map_layout_commands(cls.layout_data, cls.mock_commands)
        except FileNotFoundError:
            cls.fail("ERROR: layout_enhanced.yaml not found. Cannot run tests.")
        except Exception as e:
            cls.fail(f"ERROR loading/parsing layout_enhanced.yaml: {e}")

    @classmethod
    def map_layout_commands(cls, layout_data, mapping):
        """Helper to simulate command mapping (copied from demo_app_yaml.py)."""
        if isinstance(layout_data, dict):
            for key, value in layout_data.items():
                if key == "command" and isinstance(value, str):
                    if value in mapping:
                        layout_data[key] = mapping[value]
                    else:
                        # In tests, we might want to fail or just ignore missing commands
                        print(f"Warning: Command '{value}' in layout not in mock_commands.")
                        layout_data[key] = None
                else:
                    cls.map_layout_commands(value, mapping) # Recurse
        elif isinstance(layout_data, list):
            for item in layout_data:
                cls.map_layout_commands(item, mapping)

    def setUp(self):
        """Set up a fresh Tk root and SimpleGUI instance for each test."""
        self.root = tk.Tk()
        # Prevent the window from actually appearing during tests
        self.root.withdraw()
        self.app = SimpleGUI(self.root, title="Test App", size="600x400")
        # Reset mocks before each test
        for cmd_mock in self.mock_commands.values():
            cmd_mock.reset_mock()

    def tearDown(self):
        """Destroy the Tk root window after each test."""
        if self.root:
            self.root.destroy()
        # Ensure patches are stopped if applied per-test
        # (Here they are applied per-class or via decorators)

    # --- Test Cases ---

    def test_01_build_app_without_errors(self):
        """Test if the GUI builds completely from the enhanced layout without raising errors."""
        try:
            # Apply PIL mocks for Picture widget creation
            with pil_available_patch, pil_open_patch, pil_photoimage_patch:
                 self.app.build(self.layout_data)
        except Exception as e:
            self.fail(f"app.build() raised exception unexpectedly: {e}")

    @pil_available_patch
    @pil_open_patch
    @pil_photoimage_patch
    def test_02_picture_widget_created(self, mock_pi, mock_open, mock_avail):
        """Test if the Picture widget is created and configured."""
        self.app.build(self.layout_data)
        widget = self.app.get_widget("app_logo")
        self.assertIsNotNone(widget, "Picture widget 'app_logo' not found.")
        self.assertIsInstance(widget, Picture, "Widget 'app_logo' is not a Picture instance.")
        # Check if Image.open was called with the correct path from YAML
        mock_open.assert_called_once_with("logo.png")
        # Check if resize was called based on YAML options (width: 64)
        # The mock resize returns the same mock, check if it was called
        mock_image.resize.assert_called_with((64, 64), ANY) # Height calculated from aspect ratio
        # Check if PhotoImage was created with the (resized) image mock
        mock_pi.assert_called_once_with(mock_image)
        # Check if the widget's image option was set
        widget_img = widget.cget("image")
        # The actual image object reference might be tricky to compare directly with mock
        self.assertTrue(str(widget_img).startswith(str(mock_photo_image).split()[0]), "Widget image not set correctly.")


    @patch('simplegui.custom_widgets.PIL_AVAILABLE', True) # Assume PIL is available
    @patch('simplegui.custom_widgets.Image.open', side_effect=FileNotFoundError("Mock File Not Found"))
    def test_03_picture_widget_file_not_found(self, mock_open, mock_avail):
        """Test Picture widget behavior when the image file is not found."""
        self.app.build(self.layout_data)
        widget = self.app.get_widget("app_logo")
        self.assertIsNotNone(widget)
        self.assertIsInstance(widget, Picture)
        # Check if error message is displayed (implementation specific)
        self.assertIn("Error: File not found", widget.cget("text"))
        self.assertEqual(widget.cget("fg"), "red")
        mock_open.assert_called_once_with("logo.png")

    @patch('simplegui.custom_widgets.PIL_AVAILABLE', False) # Mock PIL as unavailable
    def test_04_picture_widget_pillow_not_available(self, mock_avail):
        """Test Picture widget behavior when Pillow is not installed."""
        self.app.build(self.layout_data)
        widget = self.app.get_widget("app_logo")
        self.assertIsNotNone(widget)
        self.assertIsInstance(widget, Picture)
        self.assertIn("Error: Pillow not installed", widget.cget("text"))
        self.assertEqual(widget.cget("fg"), "red")

    def test_05_separator_widget_created(self):
        """Test if the Separator widget is created."""
        self.app.build(self.layout_data)
        # Separators usually don't have names in this layout, find by type/parent
        # Let's find the main container frame first
        main_container = self.root.winfo_children()[0] # Assumes first child is the main frame
        separator_found = False
        for child in main_container.winfo_children(): # Iterate through row frames
             for widget in child.winfo_children(): # Iterate widgets in row
                 if isinstance(widget, ttk.Separator):
                     separator_found = True
                     self.assertEqual(widget.cget("orient"), "horizontal") # Check option from YAML
                     break
             if separator_found:
                 break
        self.assertTrue(separator_found, "ttk.Separator widget not found in the layout.")


    def test_06_notebook_widget_created(self):
        """Test if the Notebook widget and its tabs are created."""
        self.app.build(self.layout_data)
        notebook = self.app.get_widget("main_notebook")
        self.assertIsNotNone(notebook, "Notebook widget 'main_notebook' not found.")
        self.assertIsInstance(notebook, ttk.Notebook, "Widget 'main_notebook' is not a ttk.Notebook.")

        tabs = notebook.tabs()
        self.assertEqual(len(tabs), 3, "Notebook should have 3 tabs.")

        # Check tab titles (Note: .tab() needs the tab_id, which is the frame inside)
        tab_frames = [notebook.nametowidget(tab_id) for tab_id in tabs]
        self.assertEqual(notebook.tab(tab_frames[0], "text"), "Registrierung")
        self.assertEqual(notebook.tab(tab_frames[1], "text"), "Datentabelle")
        self.assertEqual(notebook.tab(tab_frames[2], "text"), "Weitere Widgets")

    def test_07_widgets_inside_notebook_created(self):
        """Test if widgets defined within Notebook tabs are created."""
        self.app.build(self.layout_data)
        # Check a widget from Tab 1
        username_entry = self.app.get_widget("username_entry")
        self.assertIsNotNone(username_entry, "Widget 'username_entry' inside Notebook Tab 1 not found.")
        self.assertIsInstance(username_entry, tk.Entry, "Widget 'username_entry' is not a tk.Entry.")

        # Check a widget from Tab 2 (Treeview)
        data_table = self.app.get_widget("data_table")
        self.assertIsNotNone(data_table, "Widget 'data_table' inside Notebook Tab 2 not found.")
        self.assertIsInstance(data_table, ttk.Treeview, "Widget 'data_table' is not a ttk.Treeview.")

        # Check a widget from Tab 3
        color_combo = self.app.get_widget("color_combo")
        self.assertIsNotNone(color_combo, "Widget 'color_combo' inside Notebook Tab 3 not found.")
        self.assertIsInstance(color_combo, ttk.Combobox, "Widget 'color_combo' is not a ttk.Combobox.")
        self.assertEqual(color_combo['values'], ("Rot", "Grün", "Blau", "Gelb")) # Check values option

    def test_08_treeview_widget_created_and_configured(self):
        """Test if the Treeview widget is created with correct columns and headings."""
        self.app.build(self.layout_data)
        tree = self.app.get_widget("data_table")
        self.assertIsNotNone(tree, "Treeview widget 'data_table' not found.")
        self.assertIsInstance(tree, ttk.Treeview)

        # Check columns configuration
        expected_columns = ("id", "name", "value")
        self.assertEqual(tree['columns'], expected_columns)

        # Check headings configuration
        self.assertEqual(tree.heading("id", "text"), "ID")
        self.assertEqual(tree.heading("name", "text"), "Name")
        self.assertEqual(tree.heading("value", "text"), "Wert")

        # Check show option (removes the '#' tree column visibility)
        self.assertEqual(tree['show'], "headings")

        # Check column widths and anchors (optional but good)
        self.assertEqual(tree.column("id", "width"), 50)
        self.assertEqual(tree.column("id", "anchor"), "center")
        self.assertEqual(tree.column("name", "width"), 150)
        self.assertEqual(tree.column("name", "anchor"), "w") # Default anchor if not specified
        self.assertEqual(tree.column("value", "width"), 100)
        self.assertEqual(tree.column("value", "anchor"), "e")

        # Check scrollbar integration (indirectly by checking parent structure)
        tree_parent = tree.master
        self.assertIsInstance(tree_parent, tk.Frame) # Should be inside the container frame
        siblings = tree_parent.winfo_children()
        self.assertIn(tree, siblings)
        # Check if scrollbars are siblings
        has_v_scroll = any(isinstance(w, ttk.Scrollbar) and w.cget('orient') == 'vertical' for w in siblings)
        has_h_scroll = any(isinstance(w, ttk.Scrollbar) and w.cget('orient') == 'horizontal' for w in siblings)
        self.assertTrue(has_v_scroll, "Vertical scrollbar missing for Treeview.")
        self.assertTrue(has_h_scroll, "Horizontal scrollbar missing for Treeview.")


    def test_09_treeview_helper_methods(self):
        """Test the Treeview helper methods: insert, clear, get_item, get_value (selection)."""
        self.app.build(self.layout_data)
        tree_name = "data_table"
        tree = self.app.get_widget(tree_name)
        self.assertIsNotNone(tree)

        # Test Insert
        item_id1 = self.app.insert_treeview_item(tree_name, values=(1, 'Test A', 100))
        item_id2 = self.app.insert_treeview_item(tree_name, values=(2, 'Test B', 200))
        self.assertIsNotNone(item_id1)
        self.assertIsNotNone(item_id2)
        self.assertEqual(len(tree.get_children()), 2)

        # Test Get Item
        item1_data = self.app.get_treeview_item(tree_name, item_id1)
        self.assertEqual(item1_data['values'], [1, 'Test A', 100]) # Values are returned as list of strings by default

        # Test Get Value (Selection) - Select an item first
        tree.selection_set(item_id2)
        selected_ids = self.app.get_widget_value(tree_name)
        self.assertEqual(selected_ids, (item_id2,)) # Returns a tuple of selected IDs

        # Test Clear
        self.app.clear_treeview(tree_name)
        self.assertEqual(len(tree.get_children()), 0)

    def test_10_command_mapping_and_invocation(self):
        """Test if string commands are mapped and can be invoked."""
        self.app.build(self.layout_data)

        # Test a button outside the notebook
        exit_button = self.app.get_widget("exit_button")
        self.assertIsNotNone(exit_button)
        exit_button.invoke() # Simulate button click
        self.mock_commands["exit_app"].assert_called_once()

        # Test a button inside the notebook (Tab 1)
        register_button = self.app.get_widget("register_button")
        self.assertIsNotNone(register_button)
        register_button.invoke()
        self.mock_commands["register_user"].assert_called_once()

        # Test another button inside the notebook (Tab 2)
        populate_button = self.app.get_widget("populate_button")
        self.assertIsNotNone(populate_button)
        populate_button.invoke()
        self.mock_commands["populate_treeview"].assert_called_once()

    def test_11_get_and_set_widget_values(self):
        """Test getting and setting values for various widgets."""
        self.app.build(self.layout_data)

        # Entry (inside Tab 1)
        entry_name = "username_entry"
        self.app.set_widget_option(entry_name, "value", "TestUser") # Set via variable
        self.assertEqual(self.app.get_widget_value(entry_name), "TestUser")
        self.app.set_widget_option(entry_name, "text", "NewUser") # Set via text option
        self.assertEqual(self.app.get_widget_value(entry_name), "NewUser")


        # Checkbutton (inside Tab 1)
        check_name = "terms_check"
        self.app.set_widget_option(check_name, "value", 1)
        self.assertEqual(self.app.get_widget_value(check_name), 1)
        self.app.set_widget_option(check_name, "value", 0)
        self.assertEqual(self.app.get_widget_value(check_name), 0)

        # Combobox (inside Tab 3)
        combo_name = "color_combo"
        self.app.set_widget_option(combo_name, "value", "Grün")
        self.assertEqual(self.app.get_widget_value(combo_name), "Grün")
        # Test setting values list
        new_colors = ["Orange", "Purple"]
        self.app.set_widget_option(combo_name, "values", new_colors)
        self.assertEqual(self.app.get_widget(combo_name)['values'], tuple(new_colors))


        # Scale (inside Tab 3)
        scale_name = "rating_scale"
        self.app.set_widget_option(scale_name, "value", 7.5)
        self.assertEqual(self.app.get_widget_value(scale_name), 7.5)

        # Spinbox (inside Tab 3)
        spin_name = "count_spin"
        self.app.set_widget_option(spin_name, "value", 55)
        self.assertEqual(self.app.get_widget_value(spin_name), "55") # Spinbox value often string

        # Label (inside Tab 3) - setting text
        label_name = "info_label"
        self.app.set_widget_option(label_name, "text", "Updated Info")
        self.assertEqual(self.app.get_widget(label_name).cget("text"), "Updated Info")


# --- Run Tests ---
if __name__ == '__main__':
    unittest.main()

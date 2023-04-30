import customtkinter as ctk
from PIL import Image, ImageTk
from processor import Processor
from tkinter import filedialog, messagebox


# Configure application theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# App class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("R&R Image Editor Pro v360 Extreme Edition Beta")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create topbar frame with widgets
        self.topbar_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.topbar_frame.grid_columnconfigure(5, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(5, weight=1)

        # Top bar buttons
        self.topbar_button_open = ctk.CTkButton(self.topbar_frame, text='Open', command=self.open_image)
        self.topbar_button_open.grid(row=0, column=1, padx=10, pady=10)
        self.topbar_button_save = ctk.CTkButton(self.topbar_frame, text='Save', command=self.save_image)
        self.topbar_button_save.grid(row=0, column=2, padx=10, pady=10)
        self.topbar_button_revert = ctk.CTkButton(self.topbar_frame, text='Revert', command=self.revert_image)
        self.topbar_button_revert.grid(row=0, column=3, padx=10, pady=5)
        self.topbar_button_undo = ctk.CTkButton(self.topbar_frame, text='Undo', command=self.undo_image)
        self.topbar_button_undo.grid(row=0, column=4, padx=10, pady=5)
        self.topbar_combobox_appearance = ctk.CTkOptionMenu(self.topbar_frame, values=["System", "Light", "Dark"],
                                                            command=self.change_appearance_mode_event,
                                                            state='readonly')
        self.topbar_combobox_appearance.grid(row=0, column=6, padx=10, pady=10)

        # Side bar buttons
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Options")
        self.scrollable_frame.grid(row=1, column=0, pady=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Flip
        self.flip_label = ctk.CTkLabel(self.scrollable_frame, text="Flip", font=ctk.CTkFont(size=20, weight="normal"))
        self.flip_label.grid(row=0, column=0, padx=20, pady=(0, 5))
        self.sidebar_switch_flip_horizontal = ctk.CTkSwitch(self.scrollable_frame, text='Horizontal', command=lambda: self.flip_image('HORIZONTAL'))
        self.sidebar_switch_flip_horizontal.grid(row=1, column=0, padx=10)
        self.sidebar_switch_flip_vertical = ctk.CTkSwitch(self.scrollable_frame, text='Vertical', command=lambda: self.flip_image('VERTICAL'))
        self.sidebar_switch_flip_vertical.grid(row=2, column=0, padx=10)

        # Bright
        self.sidebar_label_bright = ctk.CTkLabel(self.scrollable_frame, text="Bright", font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_bright.grid(row=3, column=0, padx=20, pady=(20, 5))
        self.sidebar_slider_bright = ctk.CTkSlider(self.scrollable_frame, command=self.brightness_filter)
        self.sidebar_slider_bright.grid(row=4, column=0, padx=10)

        # Contrast
        self.sidebar_label_contrast = ctk.CTkLabel(self.scrollable_frame, text="Contrast",
                                                 font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_contrast.grid(row=5, column=0, padx=20, pady=(20, 5))
        self.sidebar_slider_contrast = ctk.CTkSlider(self.scrollable_frame, command=self.contrast_filter)
        self.sidebar_slider_contrast.grid(row=6, column=0, padx=10)

        # Grayscale and negative filter
        self.sidebar_label_filter = ctk.CTkLabel(self.scrollable_frame, text="Filtros", font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_filter.grid(row=7, column=0, padx=20, pady=(20, 5))
        self.sidebar_switch_grayscale = ctk.CTkSwitch(self.scrollable_frame, text='Grayscale', command=self.grayscale_filter)
        self.sidebar_switch_grayscale.grid(row=8, column=0, padx=10)
        self.sidebar_switch_negative = ctk.CTkSwitch(self.scrollable_frame, text='Negative', command=self.negative_filter)
        self.sidebar_switch_negative.grid(row=9, column=0, padx=10)

        # Rotate
        self.sidebar_label_rotate = ctk.CTkLabel(self.scrollable_frame, text="Rotate",
                                                   font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_rotate.grid(row=10, column=0, padx=20, pady=(20, 5))
        self.sidebar_button_rotate = ctk.CTkButton(self.scrollable_frame, text='Rotate', command=self.rotate_image)
        self.sidebar_button_rotate.grid(row=11, column=0, padx=10)

        # Move
        self.sidebar_label_move = ctk.CTkLabel(self.scrollable_frame, text="Move",
                                               font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_move.grid(row=12, column=0, padx=20, pady=(20, 5))
        self.sidebar_button_move_horizontal = ctk.CTkButton(self.scrollable_frame, text='Horizontal', command=lambda: self.move_image('HORIZONTAL'))
        self.sidebar_button_move_horizontal.grid(row=13, column=0, padx=10, pady=5)
        self.sidebar_button_move_vertical = ctk.CTkButton(self.scrollable_frame, text='Vertical', command=lambda: self.move_image('VERTICAL'))
        self.sidebar_button_move_vertical.grid(row=14, column=0, padx=10, pady=5)

        # Resize
        self.sidebar_label_resize = ctk.CTkLabel(self.scrollable_frame, text="Resize",
                                               font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_resize.grid(row=15, column=0, padx=20, pady=(20, 5))
        self.sidebar_button_resize_width = ctk.CTkButton(self.scrollable_frame, text='Width',
                                                            command=lambda: self.resize_image('WIDTH'))
        self.sidebar_button_resize_width.grid(row=16, column=0, padx=10, pady=5)
        self.sidebar_button_resize_height = ctk.CTkButton(self.scrollable_frame, text='Height',
                                                          command=lambda: self.resize_image('HEIGHT'))
        self.sidebar_button_resize_height.grid(row=17, column=0, padx=10, pady=5)

        # Operations
        self.sidebar_label_operations = ctk.CTkLabel(self.scrollable_frame, text="Operations",
                                                     font=ctk.CTkFont(size=20, weight="normal"))
        self.sidebar_label_operations.grid(row=18, column=0, padx=20, pady=(20, 5))
        self.sidebar_combobox_operations = ctk.CTkOptionMenu(self.scrollable_frame,
                                                             values=['Sum', 'Subtract', 'AND', 'OR'],
                                                             command=self.operations,
                                                             state='readonly')
        self.sidebar_combobox_operations.grid(row=19, column=0, padx=10, pady=5)

        self.image_preview_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.image_preview_frame.grid(row=1, column=1, sticky="nsew")
        self.image_preview_frame.grid_columnconfigure(1, weight=1)

        self.image_label = ctk.CTkLabel(self.image_preview_frame,
                                        text='',
                                        image=None)
        self.image_label.grid(row=0, column=1, padx=20, pady=10)

        # Set default values
        self.disable_buttons()

        # Processor class
        self.processor = Processor()

    def open_input_dialog_event(self, message, title):
        """Get input from user"""
        dialog = ctk.CTkInputDialog(text=message, title=title)
        return dialog.get_input()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change window style"""
        ctk.set_appearance_mode(new_appearance_mode)

    def update_label_image(self):
        """Update image label"""
        _image = Image.fromarray(self.processor.image, 'RGB')
        h = _image.height
        w = _image.width

        window_shape = (720, 480)

        if w > window_shape[0]:
            _scale = w / window_shape[0]
            w = window_shape[0]
            h /= _scale

        if h > window_shape[1]:
            _scale = h / window_shape[1]
            h = window_shape[1]
            w /= _scale

        _image = ctk.CTkImage(_image, size=(w, h))
        self.image_label.configure(image=_image)

    def disable_buttons(self):
        """Disable all buttons"""
        for child in self.scrollable_frame.winfo_children():
            try:
                child.configure(state='disabled')
            except:
                pass

        self.topbar_button_save.configure(state="disabled")
        self.topbar_button_undo.configure(state="disabled")
        self.topbar_button_revert.configure(state="disabled")

    def enable_buttons(self):
        """Enable all buttons"""
        for child in self.scrollable_frame.winfo_children():
            try:
                child.configure(state='normal')
            except:
                pass

        self.topbar_button_save.configure(state="normal")
        self.topbar_button_undo.configure(state="normal")
        self.topbar_button_revert.configure(state="normal")

    def open_image_ask(self):
        """Open a filedialog to select the filename to open"""
        try:
            file_types = [("JPEG", "*.jpg"), ("PNG", "*.png")]
            filename = filedialog.askopenfilename(initialdir='~/Pictures', title='Open image', filetypes=file_types)
            return None if filename == '' else filename
        except(OSError, FileNotFoundError):
            messagebox.showerror('Error', 'Unable to find or open file <filename>')
        except Exception as error:
            messagebox.showerror('Error', 'An error occurred: <error>')

    def open_image(self):
        """Open askopen filename to select the image"""
        filename = self.open_image_ask()
        if filename is not None:
            try:
                self.processor.open_image(filename)
                self.update_label_image()
                self.enable_buttons()
            except:
                messagebox.showerror('Error', 'An error occurred while opening the file!')

    def undo_image(self):
        """Return back last action in the image"""
        self.processor.undo_image()
        self.update_label_image()

    def revert_image(self):
        """Return back all actions in the image"""
        self.processor.revert_image()
        self.update_label_image()

    def save_image(self):
        """Save a result image in a specific location"""
        file_types = [("JPEG", "*.jpg"), ("PNG", "*.png")]
        location = filedialog.asksaveasfilename(initialdir='~/Pictures', title='Save image', filetypes=file_types,
                                                defaultextension='')
        if location is not None:
            try:
                self.processor.save_image(location)
            except:
                messagebox.showerror('Error!', 'An error ocurred while saving the image!')

    def move_image(self, option):
        """Move an image"""
        try:
            amount = int(self.open_input_dialog_event('Type the amount to move:', 'Move'))
            self.processor.move_image(option, amount)
            self.update_label_image()
        except:
            messagebox.showerror('Error', 'The amount need to be a real number!')

    def resize_image(self, option):
        """Resize an image"""
        try:
            amount = int(self.open_input_dialog_event('Type the amount to sum:', 'Resize'))
            self.processor.resize_image(option, amount)
            self.update_label_image()
        except ValueError as e:
            messagebox.showerror('Error', 'The amount need to be a real number!')
        except:
            messagebox.showerror('Error', 'The size cannot be less than 0!')

    def rotate_image(self):
        """Rotate an image"""
        try:
            degrees = int(self.open_input_dialog_event('Type the degrees to rotate (counter-clockwise):',
                                                       'Rotate'))
            self.processor.rotate_image(degrees)
            self.update_label_image()
        except:
            messagebox.showerror('Error', 'The degrees need to be a real number!')

    def negative_filter(self):
        """Aplies negative filter to an image"""
        self.processor.negative_filter()
        self.update_label_image()

    def grayscale_filter(self):
        """Aplies grayscale filter to an image"""
        self.processor.grayscale_filter()
        self.update_label_image()

    def flip_image(self, option):
        """Flip image horizontal or vertical"""
        self.processor.flip_image(option)
        self.update_label_image()

    def contrast_filter(self, gain):
        """Aplies contrast filter to an image"""
        self.processor.contrast_filter(gain)
        self.update_label_image()

    def brightness_filter(self, bias):
        """Aplies brightness filter to an image"""
        self.processor.brightness_filter(bias)
        self.update_label_image()

    def operations(self, option):
        """Aplies an operation into the image"""
        another = self.open_image_ask()
        if another is not None:
            self.processor.operations(option, another)
            self.update_label_image()


if __name__ == "__main__":
    app = App()
    app.mainloop()

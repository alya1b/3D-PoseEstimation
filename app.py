import tkinter
import customtkinter
import os
import webbrowser
from tkinter import filedialog
from Solver import Solver
from PIL import Image
import tempfile

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.Solver = Solver()

        # configure window
        self.title("Body Movements Analyzer")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Adjusted row configuration
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Analyzer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")  # Adjusted sticky attribute
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")  # Adjusted pady and sticky attributes
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")  # Adjusted sticky attribute
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")  # Adjusted pady and sticky attributes

        # create tabview for exercises
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Гоніометрія кульшового суглоба")
        self.tabview.add("Гоніометрія кульшового суглоба(л)")
        self.tabview.add("Рухи в плечі")
        self.tabview.tab("Гоніометрія кульшового суглоба").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Гоніометрія кульшового суглоба(л)").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Рухи в плечі").grid_columnconfigure(0, weight=1)

        # Add elements to Exercise 1 tab
        self.add_elements_to_exercise1_tab()
        # Keep track of the currently selected tab
        self.current_tab_name = "Гоніометрія кульшового суглоба"

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def add_elements_to_exercise1_tab(self):
        exercise1_tab = self.tabview.tab("Гоніометрія кульшового суглоба")
        
        # Add heading and example text
        heading_label = customtkinter.CTkLabel(exercise1_tab, text="Гоніометрія кульшового суглоба (правий)", font=customtkinter.CTkFont(size=16, weight="bold"))
        heading_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        example_text = "Вимірювання флексії, екстензії, приведення і відведення, внутрішньої та зовнішньої ротації в кульшовому суглобі"
        example_label = customtkinter.CTkLabel(exercise1_tab, text=example_text, wraplength=400)
        example_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # Add instruction button
        instruction_button = customtkinter.CTkButton(exercise1_tab, text="Інструкція", command=self.open_instruction)
        instruction_button.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Store selected file paths
        self.selected_files = [""] * 6

        # Add position selection and file load option
        positions = ["Флексія", "Екстензія", "Приведення", "Відведення", "Внутрашня ротація", "Зовнішня ротація"]
        for i, position in enumerate(positions, start=1):
            position_label = customtkinter.CTkLabel(exercise1_tab, text=position, font=customtkinter.CTkFont(size=14, weight="bold"))
            position_label.grid(row=i+2, column=0, padx=20, pady=(10, 5), sticky="w")
            self.selected_files[i - 1] = tkinter.StringVar(value="No file selected")
            file_label = customtkinter.CTkLabel(exercise1_tab, textvariable=self.selected_files[i - 1])
            file_label.grid(row=i+2, column=1, padx=20, pady=(10, 5), sticky="w")
            file_button = customtkinter.CTkButton(exercise1_tab, text=f"Load file for {position}", command=lambda idx=i: self.load_file(idx))
            file_button.grid(row=i+2, column=2, padx=10, pady=(10, 5), sticky="w")

        # Add submit button
        submit_button = customtkinter.CTkButton(exercise1_tab, text="Submit", command=self.submit_files)
        submit_button.grid(row=len(positions) + 3, column=2, padx=20, pady=20, sticky="se")

    def open_instruction(self):
        instruction_path = os.path.join(os.getcwd(), 'documents', 'Instruction-1.pdf')
        webbrowser.open_new(r'file://' + instruction_path)

    def load_file(self, position_idx):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            file_name = os.path.basename(file_path)
            self.selected_files[position_idx - 1].set(file_name)

    def submit_files(self):
        # Gather file paths
        file_paths = [file_var.get() for file_var in self.selected_files]

        # Send data to solver and get the review
        review_text_parts, images = self.Solver.generate_review(self.current_tab_name, file_paths)

        # Create a new window to display the review
        review_window = customtkinter.CTkToplevel(self)
        review_window.title("Review")
        review_window.geometry("800x600")  # Adjust size as needed

        # Add heading for the review
        heading_label = customtkinter.CTkLabel(review_window, text="Аналіз гоніометрії кульшового суглоба", font=customtkinter.CTkFont(size=18, weight="bold"))
        heading_label.pack(anchor="w", padx=20, pady=10)

        # Create a scrollable frame to hold the text and images
        scrollable_frame = customtkinter.CTkScrollableFrame(review_window)
        scrollable_frame.pack(fill="both", expand=True)

        for text_part, img in zip(review_text_parts, images):
            # Display text in a Label widget
            text_label = customtkinter.CTkLabel(scrollable_frame, text=text_part, font=customtkinter.CTkFont(size=14), wraplength=600, justify="left")
            text_label.pack(anchor="w", pady=(10, 5))

            # Save the PIL image to a temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            img.save(temp_file.name)

            # Load the temporary file using Tkinter
            img_tk = tkinter.PhotoImage(file=temp_file.name)
            img_label = tkinter.Label(scrollable_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.pack(anchor="w", pady=(5, 10))

        # Add a close button to close the window
        close_button = customtkinter.CTkButton(scrollable_frame, text="Close", command=review_window.destroy)
        close_button.pack(pady=(10, 10))

if __name__ == "__main__":
    app = App()
    app.mainloop()

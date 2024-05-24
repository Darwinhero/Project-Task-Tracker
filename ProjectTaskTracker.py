import tkinter as tk
from tkinter import messagebox, Toplevel, Button, END
from datetime import datetime
import ctypes


# Define a custom Entry widget with placeholder text support
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        # Initialize the Entry widget
        super().__init__(master, *args, **kwargs)

        # Set the placeholder text
        self.placeholder = placeholder

        # Set the placeholder text color
        self.placeholder_color = "grey"

        # Store the default text color
        self.default_color = self["fg"]

        # Bind the on_focus_in method to the FocusIn event
        self.bind("<FocusIn>", self.on_focus_in)

        # Bind the on_focus_out method to the FocusOut event
        self.bind("<FocusOut>", self.on_focus_out)

        # Display the placeholder text initially
        self.put_placeholder()

    # Method to display the placeholder text
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color

    # Event handler for when the entry gets focus
    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self["fg"] = self.default_color

    # Event handler for when the entry loses focus
    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()


# Main application class for the Project Task Tracker
class ProjectTaskTracker:
    def __init__(self):
        # Create the main application window
        self.root = tk.Tk()

        # Set the window title
        self.root.title("Project Task Tracker")

        # Get screen width and height using ctypes module
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        # Set window size to three-fourth of the screen
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.root.geometry(f"{window_width}x{window_height}")

        # Set background color for the main window
        self.root.config(bg="#f5f5f5")

        # Create a title label for the application
        self.title_label = tk.Label(self.root, text="Project Task Tracker", font=("Arial", 20, "bold"), bg="#f5f5f5")
        self.title_label.pack(pady=20)

        # Create labels and entry fields for project name, description, and time scheduled
        self.project_label = tk.Label(self.root, text="Project Name:", font=("Arial", 12), bg="#f5f5f5")
        self.project_label.pack(pady=(0, 5), padx=20, anchor="w")
        self.project_entry = tk.Entry(self.root, font=("Arial", 12))
        self.project_entry.pack(pady=(0, 10), padx=20, ipady=5, ipadx=10)

        self.description_label = tk.Label(self.root, text="Project Description:", font=("Arial", 12), bg="#f5f5f5")
        self.description_label.pack(pady=(0, 5), padx=20, anchor="w")
        self.description_entry = tk.Entry(self.root, font=("Arial", 12))
        self.description_entry.pack(pady=(0, 10), padx=20, ipady=5, ipadx=10)

        self.time_label = tk.Label(self.root, text="Time Scheduled (hour:minute, month-day-year):", font=("Arial", 12),
                                   bg="#f5f5f5")
        self.time_label.pack(pady=(0, 5), padx=20, anchor="w")

        # Use the custom PlaceholderEntry widget for the time entry field
        self.time_entry = PlaceholderEntry(self.root, placeholder="E.g., 10:30, 05-23-2024", width=40,
                                           font=("Arial", 12))
        self.time_entry.pack(pady=(0, 20), padx=20, ipady=5, ipadx=10)

        # Create buttons for adding projects, viewing projects, and logging out
        self.add_button = tk.Button(self.root, text="Add Project", command=self.add_project, font=("Arial", 12, "bold"),
                                    bg="#4caf50", fg="white")
        self.add_button.pack(pady=(0, 20), padx=20, ipady=5, ipadx=10, anchor="w")

        self.view_button = tk.Button(self.root, text="View Projects", command=self.view_projects,
                                     font=("Arial", 12, "bold"), bg="#2196f3", fg="white")
        self.view_button.pack(pady=(0, 20), padx=20, ipady=5, ipadx=10, anchor="w")

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 12, "bold"),
                                       bg="#f44336", fg="white")
        self.logout_button.pack(pady=(0, 20), padx=20, ipady=5, ipadx=10, anchor="w")

        # List to store projects
        self.projects = []

        # Start the main event loop
        self.root.mainloop()

    # Method to add a new project
    def add_project(self):
        project_name = self.project_entry.get()
        description = self.description_entry.get()
        time_scheduled = self.time_entry.get()
        if project_name and self.validate_time_format(time_scheduled):
            self.projects.append((project_name, description, time_scheduled))
            messagebox.showinfo("Success", "Project added successfully!")
            # Clear entry fields after adding project
            self.project_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
            self.time_entry.delete(0, "end")
            self.time_entry.put_placeholder()
        else:
            messagebox.showerror("Error", "Please enter both project name and time scheduled in the correct format.")

    # Method to view all added projects
    def view_projects(self):
        if not self.projects:
            messagebox.showinfo("No Projects", "No projects added yet.")
            return

        view_window = tk.Toplevel(self.root)
        view_window.title("View Projects")

        # Set window size to three-fourth of the screen
        view_window_width = int(self.root.winfo_screenwidth() * 0.75)
        view_window_height = int(self.root.winfo_screenheight() * 0.75)
        view_window.geometry(f"{view_window_width}x{view_window_height}")

        # Set background color
        view_window.config(bg="#f5f5f5")

        # Title Label
        title_label = tk.Label(view_window, text="Projects", font=("Arial", 16, "bold"), bg="#f5f5f5")
        title_label.pack(pady=10)

        # Frame to contain project information
        project_frame = tk.Frame(view_window, bg="#f5f5f5")
        project_frame.pack(pady=10, padx=20)

        for idx, project in enumerate(self.projects, start=1):
            # Project Name
            project_name_label = tk.Label(project_frame, text=f"Project Name:\n{project[0]}", font=("Arial", 12),
                                          bg="#f5f5f5")
            project_name_label.grid(row=idx, column=0, sticky="w")

            # Project Description
            project_description_label = tk.Label(project_frame, text=f"Description:\n{project[1]}", font=("Arial", 12),
                                                 bg="#f5f5f5")
            project_description_label.grid(row=idx, column=1, sticky="w")

            # Time Scheduled
            project_time_label = tk.Label(project_frame, text=f"Time Scheduled:\n{project[2]}", font=("Arial", 12),
                                          bg="#f5f5f5")
            project_time_label.grid(row=idx, column=2, sticky="w")

            # Delete Button
            delete_button = tk.Button(project_frame, text="Delete", command=lambda idx=idx: self.delete_project(idx),
                                      font=("Arial", 10, "bold"), bg="#f44336", fg="white")
            delete_button.grid(row=idx, column=3, padx=5)

    # Method to delete a project
    def delete_project(self, idx):
        del self.projects[idx - 1]
        messagebox.showinfo("Success", "Project deleted successfully.")
        self.refresh_view_projects()

    # Method to refresh the project view
    def refresh_view_projects(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__()

    # Method to validate the format of the time string
    def validate_time_format(self, time_str):
        try:
            datetime.strptime(time_str, "%H:%M, %m-%d-%Y")
            return True
        except ValueError:
            return False

    # Method to handle logout functionality
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            open_login_window()


# Function to open the login window
def open_login_window():
    login_window = tk.Tk()
    login_window.title("Login Form")

    # Set window size to half of the screen
    window_width = int(login_window.winfo_screenwidth() * 0.5)
    window_height = int(login_window.winfo_screenheight() * 0.5)
    login_window.geometry(f"{window_width}x{window_height}")

    # Callback function for successful login
    def on_login_success():
        login_window.destroy()
        ProjectTaskTracker()

    # Callback function for failed login
    def on_login_failure():
        messagebox.showerror("Error", "Invalid username or password!")

    # Method to authenticate the user
    def authenticate(username, password):
        if username == "aljames" and password == "letsgo":
            print("Login Successful!")
            on_login_success()
        else:
            on_login_failure()

    # Set background color for the login window
    login_window.config(bg="#f5f5f5")

    # Username Label and Entry
    username_label = tk.Label(login_window, text="Username:", font=("Arial", 12), bg="#f5f5f5")
    username_label.pack(pady=5, padx=20, anchor="w")
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5, padx=20, ipady=5, ipadx=10)

    # Password Label and Entry
    password_label = tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#f5f5f5")
    password_label.pack(pady=5, padx=20, anchor="w")
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5, padx=20, ipady=5, ipadx=10)

    # Login Button
    login_button = tk.Button(login_window, text="Login",
                             command=lambda: authenticate(username_entry.get(), password_entry.get()),
                             font=("Arial", 12, "bold"), bg="#4caf50", fg="white")
    login_button.pack(pady=10, padx=20, ipady=5, ipadx=10, anchor="w")

    login_window.mainloop()


# Check if the script is being run directly
if __name__ == "__main__":
    open_login_window()
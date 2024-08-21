import tkinter as tk 
from tkinter import ttk
import calendarFeed


class Application:
    def __init__(self, title):
        self.title = title
        self.window = tk.Tk()
        self.window.title(self.title)
        self.assignments = {}
        self.assignment_panelisEnabled = False
        if self.assignment_panelisEnabled:
            # Initialize assignment data (you can replace this with database integration)
            self.setAssignments()
            
            # Create UI elements
            self.create_widgets()
        else:
            self.requestToken()
    
    def requestToken(self):
        """ 
            Creates a frame that requests the user to enter their token. 
            
            Preferably provides a screenshot of where to go to access the token (HCC Email Calendar)

        """
        self.token_frame = tk.Frame(self.window, padx=20,pady=20)
        self.token_frame.pack()

        tk.Label(self.token_frame,text= "Please enter your token").pack()
        self.token_entry = tk.Entry(self.token_frame)
        self.token_entry.pack(pady=10)

        # submit button
        submit_button = ttk.Button (self.token_frame,text="Submit" ,command= self.on_token_submit)
        submit_button.pack(pady=20)

    def on_token_submit(self):
        self.userToken =self.token_entry.get().strip()
        # if token exists - destroy window and set up application
        if self.userToken:
            # Destroy the token request UI
            self.token_frame.destroy()
            # Proceed to initialize assignments and create widgets
            self.assignment_panelisEnabled = True
            self.setAssignments()
            self.create_widgets()
        else:
            # Show an error message or handle invalid token scenario
            tk.messagebox.showerror("Error", "Invalid token. Please try again.")

        pass

    def setAssignments(self):
        """
            Parses calendar and returns the assignmens along with asssignment title, course, due date, and status of the assignment
        """
        # TODO: Allow user to enter their own token
        cal = calendarFeed.CalendarFeed(self.userToken)
        self.assignments = cal.parseCal()
        return self.assignments

    def create_widgets(self):
        # Create a treeview widget to display assignments
        self.tree = ttk.Treeview(self.window, columns=("Title", "Course","Due Date", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Course",text="Course")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        
        
        # Insert assignments into the treeview
        for assignment in self.assignments:
            self.tree.insert("", "end", values=(assignment["title"], assignment["course"],assignment["due_date"], assignment["status"]))
        
        self.tree.pack(padx=10, pady=10)
        
        # Button to mark an assignment as submitted
        submit_button = ttk.Button(self.window, text="Mark as Submitted", command=self.mark_as_submitted)
        submit_button.pack(pady=10)
        
    def mark_as_submitted(self):
        """
        Function used to marked the selected assignment as completed
        """
        selected_item = self.tree.focus()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            item_index = self.tree.index(selected_item)
            
            # Update status to "Submitted" in the data structure
            self.assignments[item_index]["status"] = "Submitted"
            
            # Update the treeview display for the "Status" column
            self.tree.item(selected_item, values=(item_values[0], item_values[1], item_values[2], "Submitted"))
            
            # TODO: Update database here if necessary
            
            print(self.assignments[item_index]['title'])


    def run(self):
        self.window.mainloop()

# Instantiate the Application and run it
if __name__ == "__main__":
    app = Application("Assignment Tracker")
    app.run()
import tkinter as tk 
from tkinter import ttk
import calendarFeed



class Application:
    def __init__(self, title):
        self.title = title
        self.window = tk.Tk()
        self.window.title(self.title)
        self.assignments = {}

        # Initialize assignment data (you can replace this with database integration)
        self.setAssignments()
        
        # Create UI elements
        self.create_widgets()
    
    def setAssignments(self):
        
        # TODO: Allow user to enter their own token
        userToken = 'user_QjCN6kSXrjOWIfGdYN5kFpHDdpTxooTfnDxVIvIT'
        cal = calendarFeed.CalendarFeed(userToken)
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
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import calendar
import json
import os
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")
        self.root.geometry("400x400")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.marked_dates = {}  # To store marked dates and their reminders as {str(year, month, day): reminder}

        self.header_frame = ttk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, pady=10)

        self.left_button = ttk.Button(self.header_frame, text='<', command=self.prev_month)
        self.left_button.grid(row=0, column=0)

        self.month_year_label = ttk.Label(self.header_frame, text='', width=15, anchor='center')
        self.month_year_label.grid(row=0, column=1)

        self.right_button = ttk.Button(self.header_frame, text='>', command=self.next_month)
        self.right_button.grid(row=0, column=2)

        self.preview_button = ttk.Button(self.root, text='Preview Reminders', command=self.preview_reminders)
        self.preview_button.grid(row=1, column=0, pady=10)

        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.grid(row=2, column=0)

        self.show_calendar()
        self.load_reminders()

    def show_calendar(self):
        self.month_year_label.config(text=f'{calendar.month_name[self.current_month]} {self.current_year}')

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            ttk.Label(self.calendar_frame, text=day).grid(row=0, column=i)

        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        for row, week in enumerate(month_calendar, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    ttk.Label(self.calendar_frame, text='').grid(row=row, column=col)
                else:
                    label = ttk.Label(self.calendar_frame, text=str(day))
                    label.grid(row=row, column=col)
                    label.bind("<Button-1>", lambda e, day=day: self.toggle_mark(day))
                    label.bind("<Button-3>", lambda e, day=day: self.show_reminder(day))  # Right-click to show reminder

                    # Check if the date is marked and display a dot
                    if f'{self.current_year}-{self.current_month}-{day}' in self.marked_dates:
                        dot = tk.Canvas(self.calendar_frame, width=5, height=5, bg='black')
                        dot.grid(row=row, column=col, sticky='s')

    def toggle_mark(self, day):
        date_str = f'{self.current_year}-{self.current_month}-{day}'
        if date_str in self.marked_dates:
            del self.marked_dates[date_str]
        else:
            reminder = simpledialog.askstring("Add Reminder", "Enter a reminder for this date:")
            if reminder:
                self.marked_dates[date_str] = reminder
        self.show_calendar()
        self.save_reminders()

    def show_reminder(self, day):
        date_str = f'{self.current_year}-{self.current_month}-{day}'
        if date_str in self.marked_dates:
            reminder = self.marked_dates[date_str]
            messagebox.showinfo("Reminder", f"Reminder for {date_str}:\n{reminder}")
        else:
            messagebox.showinfo("Reminder", f"No reminder set for {date_str}.")

    def preview_reminders(self):
        reminders_text = ""
        for date_str, reminder in self.marked_dates.items():
            year, month, day = map(int, date_str.split('-'))
            if month == self.current_month:
                reminders_text += f"{day} {calendar.month_name[month]}: {reminder}\n"
        
        if reminders_text:
            messagebox.showinfo("Preview Reminders", reminders_text.strip())
        else:
            messagebox.showinfo("Preview Reminders", "No reminders set for this month.")

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar()

    def save_reminders(self):
        with open('remind.json', 'w') as json_file:
            json.dump(self.marked_dates, json_file, indent=4)
        print("Reminders saved to remind.json")

    def load_reminders(self):
        if os.path.exists('remind.json'):
            with open('remind.json', 'r') as json_file:
                self.marked_dates = json.load(json_file)
            self.show_calendar()
            print("Reminders loaded from remind.json")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

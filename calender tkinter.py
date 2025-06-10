import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta
import calendar


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")
        self.root.configure(bg="#ffffff")
        
        # Set window size and position
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Try to maximize window
        try:
            self.root.state("zoomed")  # Windows
        except:
            try:
                self.root.attributes("-zoomed", True)  # Linux
            except:
                pass

        self.selected_date = datetime.now()
        self.view_mode = tk.StringVar(value="Month")
        self.events = {}

        # Google Calendar color scheme
        self.colors = {
            'primary': '#1a73e8',
            'primary_light': '#4285f4',
            'background': '#ffffff',
            'surface': '#f8f9fa',
            'border': '#dadce0',
            'text_primary': '#202124',
            'text_secondary': '#5f6368',
            'hover': '#f1f3f4',
            'today': '#1a73e8',
            'today_bg': '#e8f0fe',
            'weekend': '#f8f9fa'
        }

        self.setup_styles()
        self.create_layout()
        self.refresh_view()

    def setup_styles(self):
        """Setup ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Nav.TButton', 
                       font=('Segoe UI', 9),
                       relief='flat',
                       borderwidth=1)
        
        style.configure('View.TRadiobutton',
                       font=('Segoe UI', 9),
                       background=self.colors['background'])

    def create_layout(self):
        """Create the main layout structure"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_header(main_frame)
        self.create_view_area(main_frame)

    def create_header(self, parent):
        """Create the header with navigation and view controls"""
        header_frame = tk.Frame(parent, bg=self.colors['background'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Left side - Navigation
        nav_frame = tk.Frame(header_frame, bg=self.colors['background'])
        nav_frame.pack(side=tk.LEFT, pady=15)
        
        # Navigation buttons with Google Calendar styling
        prev_btn = tk.Button(nav_frame, text="‹", 
                            font=('Segoe UI', 16, 'bold'),
                            bg=self.colors['background'],
                            fg=self.colors['text_primary'],
                            border=0,
                            padx=12, pady=6,
                            cursor='hand2',
                            command=self.prev_period)
        prev_btn.pack(side=tk.LEFT, padx=(0, 5))
        prev_btn.bind('<Enter>', lambda e: prev_btn.config(bg=self.colors['hover']))
        prev_btn.bind('<Leave>', lambda e: prev_btn.config(bg=self.colors['background']))
        
        next_btn = tk.Button(nav_frame, text="›", 
                            font=('Segoe UI', 16, 'bold'),
                            bg=self.colors['background'],
                            fg=self.colors['text_primary'],
                            border=0,
                            padx=12, pady=6,
                            cursor='hand2',
                            command=self.next_period)
        next_btn.pack(side=tk.LEFT, padx=(0, 15))
        next_btn.bind('<Enter>', lambda e: next_btn.config(bg=self.colors['hover']))
        next_btn.bind('<Leave>', lambda e: next_btn.config(bg=self.colors['background']))
        
        # Date label
        self.date_label = tk.Label(nav_frame, text="", 
                                  font=('Segoe UI', 18, 'normal'),
                                  bg=self.colors['background'],
                                  fg=self.colors['text_primary'],
                                  cursor="hand2")
        self.date_label.pack(side=tk.LEFT)
        self.date_label.bind("<Button-1>", self.show_date_selector)
        
        # Right side - View controls
        view_frame = tk.Frame(header_frame, bg=self.colors['background'])
        view_frame.pack(side=tk.RIGHT, pady=15)
        
        # View mode buttons
        month_btn = tk.Button(view_frame, text="Month",
                             font=('Segoe UI', 9),
                             bg=self.colors['primary'] if self.view_mode.get() == "Month" else self.colors['background'],
                             fg=self.colors['background'] if self.view_mode.get() == "Month" else self.colors['text_primary'],
                             border=1,
                             relief='solid',
                             padx=12, pady=6,
                             cursor='hand2',
                             command=lambda: self.change_view("Month"))
        month_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        week_btn = tk.Button(view_frame, text="Week",
                            font=('Segoe UI', 9),
                            bg=self.colors['primary'] if self.view_mode.get() == "Week" else self.colors['background'],
                            fg=self.colors['background'] if self.view_mode.get() == "Week" else self.colors['text_primary'],
                            border=1,
                            relief='solid',
                            padx=12, pady=6,
                            cursor='hand2',
                            command=lambda: self.change_view("Week"))
        week_btn.pack(side=tk.RIGHT)
        
        self.month_btn = month_btn
        self.week_btn = week_btn

    def create_view_area(self, parent):
        """Create the main view area with scrolling support"""
        # Create a frame with border
        border_frame = tk.Frame(parent, bg=self.colors['border'], padx=1, pady=1)
        border_frame.pack(fill=tk.BOTH, expand=True)
        
        self.view_frame = tk.Frame(border_frame, bg=self.colors['background'])
        self.view_frame.pack(fill=tk.BOTH, expand=True)

    def clear_view_area(self):
        """Clear the view area and reset grid configuration"""
        for widget in self.view_frame.winfo_children():
            widget.destroy()
        
        # Reset grid configuration
        for i in range(20):  # Reset more rows/columns than we typically use
            self.view_frame.grid_rowconfigure(i, weight=0, minsize=0)
            self.view_frame.grid_columnconfigure(i, weight=0, minsize=0)

    def change_view(self, mode):
        """Change view mode and update buttons"""
        self.view_mode.set(mode)
        
        # Update button styles
        if mode == "Month":
            self.month_btn.config(bg=self.colors['primary'], fg=self.colors['background'])
            self.week_btn.config(bg=self.colors['background'], fg=self.colors['text_primary'])
        else:
            self.week_btn.config(bg=self.colors['primary'], fg=self.colors['background'])
            self.month_btn.config(bg=self.colors['background'], fg=self.colors['text_primary'])
        
        self.refresh_view()

    def go_to_today(self):
        """Navigate to current date"""
        self.selected_date = datetime.now()
        self.refresh_view()

    def refresh_view(self):
        """Refresh the current view"""
        if self.view_mode.get() == "Month":
            self.show_month_view()
        else:
            self.show_week_view()

    def prev_period(self):
        """Navigate to previous period"""
        if self.view_mode.get() == "Month":
            self.prev_month()
        else:
            self.prev_week()

    def next_period(self):
        """Navigate to next period"""
        if self.view_mode.get() == "Month":
            self.next_month()
        else:
            self.next_week()

    def prev_month(self):
        """Navigate to previous month"""
        year = self.selected_date.year
        month = self.selected_date.month - 1
        if month == 0:
            month = 12
            year -= 1
        self.selected_date = self.selected_date.replace(year=year, month=month, day=1)
        self.refresh_view()

    def next_month(self):
        """Navigate to next month"""
        year = self.selected_date.year
        month = self.selected_date.month + 1
        if month == 13:
            month = 1
            year += 1
        self.selected_date = self.selected_date.replace(year=year, month=month, day=1)
        self.refresh_view()

    def prev_week(self):
        """Navigate to previous week"""
        self.selected_date -= timedelta(days=7)
        self.refresh_view()

    def next_week(self):
        """Navigate to next week"""
        self.selected_date += timedelta(days=7)
        self.refresh_view()

    def show_date_selector(self, event=None):
        """Show date selection dialog"""
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.geometry("300x200")
        top.configure(bg=self.colors['background'])
        top.grab_set()
        top.resizable(False, False)
        
        # Center the dialog
        top.transient(self.root)
        
        frame = tk.Frame(top, bg=self.colors['background'])
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(frame, text="Month:", font=('Segoe UI', 10), 
                bg=self.colors['background'], fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))
        
        month_var = tk.StringVar(value=calendar.month_name[self.selected_date.month])
        month_menu = ttk.Combobox(frame, textvariable=month_var, 
                                 values=list(calendar.month_name[1:]),
                                 state='readonly', font=('Segoe UI', 10))
        month_menu.pack(fill='x', pady=(0, 10))
        
        tk.Label(frame, text="Year:", font=('Segoe UI', 10),
                bg=self.colors['background'], fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))
        
        year_var = tk.StringVar(value=str(self.selected_date.year))
        year_entry = tk.Entry(frame, textvariable=year_var, font=('Segoe UI', 10))
        year_entry.pack(fill='x', pady=(0, 20))
        
        button_frame = tk.Frame(frame, bg=self.colors['background'])
        button_frame.pack(fill='x')
        
        def apply_change():
            try:
                selected_month = list(calendar.month_name).index(month_var.get())
                selected_year = int(year_var.get())
                self.selected_date = self.selected_date.replace(year=selected_year, month=selected_month, day=1)
                self.refresh_view()
                top.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid year.")
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              font=('Segoe UI', 9),
                              bg=self.colors['background'],
                              fg=self.colors['text_primary'],
                              border=1, relief='solid',
                              padx=15, pady=6,
                              command=top.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        apply_btn = tk.Button(button_frame, text="Apply",
                             font=('Segoe UI', 9),
                             bg=self.colors['primary'],
                             fg=self.colors['background'],
                             border=0,
                             padx=15, pady=6,
                             command=apply_change)
        apply_btn.pack(side=tk.RIGHT)

    def show_month_view(self):
        """Display month view with Google Calendar styling"""
        self.clear_view_area()
        
        year = self.selected_date.year
        month = self.selected_date.month
        today = datetime.now().date()
        
        self.date_label.config(text="{} {}".format(calendar.month_name[month], year))
        
        cal = calendar.Calendar(firstweekday=6)  # Start with Sunday
        month_days = cal.monthdatescalendar(year, month)
        
        # Day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for col, day in enumerate(days):
            header = tk.Label(self.view_frame, text=day, 
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['surface'],
                            fg=self.colors['text_secondary'],
                            padx=5, pady=12,
                            relief='solid', borderwidth=1,
                            bd=0)
            header.grid(row=0, column=col, sticky="ew")
        
        # Calendar days
        for row, week in enumerate(month_days, start=1):
            for col, date in enumerate(week):
                day_str = date.strftime("%d/%m/%Y")
                event_text = self.events.get(day_str, "")
                
                # Determine styling
                is_current_month = date.month == month
                is_today = date == today
                is_weekend = col in [0, 6]  # Sunday and Saturday
                
                # Colors
                if is_today:
                    bg_color = self.colors['today_bg']
                    text_color = self.colors['today']
                    day_font = ('Segoe UI', 10, 'bold')
                elif not is_current_month:
                    bg_color = self.colors['surface']
                    text_color = self.colors['text_secondary']
                    day_font = ('Segoe UI', 9)
                elif is_weekend:
                    bg_color = self.colors['weekend']
                    text_color = self.colors['text_primary']
                    day_font = ('Segoe UI', 9)
                else:
                    bg_color = self.colors['background']
                    text_color = self.colors['text_primary']
                    day_font = ('Segoe UI', 9)
                
                # Create day container
                day_frame = tk.Frame(self.view_frame, bg=bg_color, relief='solid', borderwidth=1, bd=0)
                day_frame.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)
                
                # Day number
                day_label = tk.Label(day_frame, text=str(date.day),
                                   font=day_font,
                                   bg=bg_color, fg=text_color,
                                   anchor='nw', padx=8, pady=6)
                day_label.pack(anchor='nw')
                
                # Event text
                if event_text:
                    event_label = tk.Label(day_frame, text=event_text,
                                         font=('Segoe UI', 8),
                                         bg=self.colors['primary'],
                                         fg=self.colors['background'],
                                         padx=4, pady=2,
                                         wraplength=80,
                                         justify='left')
                    event_label.pack(anchor='nw', padx=4, pady=(0, 4))
                
                # Make clickable
                for widget in [day_frame, day_label]:
                    widget.bind("<Button-1>", lambda e, d=day_str: self.add_event(d))
                    widget.bind("<Enter>", lambda e, f=day_frame: f.config(bg=self.colors['hover']) if f['bg'] == self.colors['background'] else None)
                    widget.bind("<Leave>", lambda e, f=day_frame, c=bg_color: f.config(bg=c))
                    widget.config(cursor='hand2')
        
        # Configure grid weights for proper resizing
        for i in range(7):
            self.view_frame.columnconfigure(i, weight=1, minsize=120)
        for i in range(len(month_days) + 1):
            self.view_frame.rowconfigure(i, weight=1, minsize=80 if i == 0 else 100)

    def show_week_view(self):
        """Display week view with Google Calendar styling"""
        self.clear_view_area()
        
        # Calculate week start (Sunday)
        current = self.selected_date
        days_since_sunday = (current.weekday() + 1) % 7
        start_of_week = current - timedelta(days=days_since_sunday)
        
        week_days = [start_of_week + timedelta(days=i) for i in range(7)]
        
        # Update header
        self.date_label.config(
            text="Week of {} - {}".format(
                start_of_week.strftime("%b %d"),
                (start_of_week + timedelta(days=6)).strftime("%b %d, %Y")
            )
        )
        
        # Time column header
        time_header = tk.Label(self.view_frame, text="",
                              bg=self.colors['surface'],
                              relief='solid', borderwidth=1, bd=0)
        time_header.grid(row=0, column=0, sticky="ew")
        
        # Day headers
        today = datetime.now().date()
        for col, day in enumerate(week_days, start=1):
            is_today = day.date() == today
            header_text = "{}\n{}".format(day.strftime("%a"), day.strftime("%d"))
            
            header = tk.Label(self.view_frame, text=header_text,
                            font=('Segoe UI', 10, 'bold' if is_today else 'normal'),
                            bg=self.colors['today_bg'] if is_today else self.colors['surface'],
                            fg=self.colors['today'] if is_today else self.colors['text_primary'],
                            relief='solid', borderwidth=1, bd=0,
                            padx=5, pady=8)
            header.grid(row=0, column=col, sticky="ew")
        
        # Time slots
        for hour in range(24):
            # Time label
            time_text = "{:02d}:00".format(hour)
            time_label = tk.Label(self.view_frame, text=time_text,
                                font=('Segoe UI', 9),
                                bg=self.colors['surface'],
                                fg=self.colors['text_secondary'],
                                anchor='ne', padx=8, pady=4,
                                relief='solid', borderwidth=1, bd=0)
            time_label.grid(row=hour + 1, column=0, sticky="ew")
            
            # Hour slots for each day
            for col, day in enumerate(week_days, start=1):
                date_str = "{} {:02d}:00".format(day.strftime("%d/%m/%Y"), hour)
                event_text = self.events.get(date_str, "")
                
                is_today = day.date() == today
                bg_color = self.colors['today_bg'] if is_today else self.colors['background']
                
                slot_frame = tk.Frame(self.view_frame, bg=bg_color,
                                    relief='solid', borderwidth=1, bd=0)
                slot_frame.grid(row=hour + 1, column=col, sticky="nsew")
                
                if event_text:
                    event_label = tk.Label(slot_frame, text=event_text,
                                         font=('Segoe UI', 8),
                                         bg=self.colors['primary'],
                                         fg=self.colors['background'],
                                         padx=4, pady=2,
                                         wraplength=100,
                                         justify='left')
                    event_label.pack(fill='both', expand=True, padx=2, pady=1)
                
                # Make clickable
                slot_frame.bind("<Button-1>", lambda e, d=date_str: self.add_event(d))
                slot_frame.bind("<Enter>", lambda e, f=slot_frame: f.config(bg=self.colors['hover']) if 'today_bg' not in str(f['bg']) else None)
                slot_frame.bind("<Leave>", lambda e, f=slot_frame, c=bg_color: f.config(bg=c))
                slot_frame.config(cursor='hand2')
        
        # Configure grid weights
        self.view_frame.columnconfigure(0, weight=0, minsize=80)
        for i in range(1, 8):
            self.view_frame.columnconfigure(i, weight=1, minsize=100)
        
        self.view_frame.rowconfigure(0, weight=0, minsize=50)
        for i in range(1, 25):
            self.view_frame.rowconfigure(i, weight=0, minsize=40)

    def add_event(self, date_str):
        """Add or edit an event"""
        current_event = self.events.get(date_str, "")
        
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Event Details")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['background'])
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.transient(self.root)
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = tk.Frame(dialog, bg=self.colors['background'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text=f"Event for {date_str}:",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 10))
        
        event_var = tk.StringVar(value=current_event)
        event_entry = tk.Entry(frame, textvariable=event_var, 
                              font=('Segoe UI', 11), width=40)
        event_entry.pack(fill='x', pady=(0, 20))
        event_entry.focus()
        
        button_frame = tk.Frame(frame, bg=self.colors['background'])
        button_frame.pack(fill='x')
        
        def save_event():
            event_text = event_var.get().strip()
            if event_text:
                self.events[date_str] = event_text
            elif date_str in self.events:
                del self.events[date_str]
            self.refresh_view()
            dialog.destroy()
        
        def delete_event():
            if date_str in self.events:
                del self.events[date_str]
                self.refresh_view()
            dialog.destroy()
        
        # Buttons
        if current_event:
            delete_btn = tk.Button(button_frame, text="Delete",
                                  font=('Segoe UI', 9),
                                  bg='#ea4335', fg=self.colors['background'],
                                  border=0, padx=15, pady=6,
                                  command=delete_event)
            delete_btn.pack(side=tk.LEFT)
        
        cancel_btn = tk.Button(button_frame, text="Cancel",
                              font=('Segoe UI', 9),
                              bg=self.colors['background'],
                              fg=self.colors['text_primary'],
                              border=1, relief='solid',
                              padx=15, pady=6,
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        save_btn = tk.Button(button_frame, text="Save",
                            font=('Segoe UI', 9),
                            bg=self.colors['primary'],
                            fg=self.colors['background'],
                            border=0, padx=15, pady=6,
                            command=save_event)
        save_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to save
        event_entry.bind('<Return>', lambda e: save_event())


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

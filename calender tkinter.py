import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import calendar
from datetime import datetime, date

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Application")
        self.root.state('zoomed')  # Full screen on Windows
        self.root.configure(bg='#f5f5f5')
        
        # Center the window and make it full screen
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', False)
        self.root.state('zoomed')
        
        self.current_year = datetime.now().year
        self.today = date.today()
        
        # Main containers
        self.main_frame = None
        self.canvas = None
        self.scrollable_frame = None
        
        self.setup_styles()
        self.show_year_dialog()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Main.TFrame', background='#f5f5f5')
        style.configure('Header.TLabel', font=('Arial', 20, 'bold'), background='#f5f5f5', foreground='#2c3e50')
        style.configure('Month.TLabel', font=('Arial', 12, 'bold'), background='#3498db', 
                       foreground='white', relief='flat', padding=5)
        style.configure('Day.TLabel', font=('Arial', 9), background='white', 
                       foreground='black', relief='solid', borderwidth=1, padding=2)
        style.configure('Weekend.TLabel', font=('Arial', 9), background='#ffebee', 
                       foreground='#e74c3c', relief='solid', borderwidth=1, padding=2)
        style.configure('Today.TLabel', font=('Arial', 9, 'bold'), background='#2ecc71', 
                       foreground='white', relief='solid', borderwidth=2, padding=2)
        style.configure('DayHeader.TLabel', font=('Arial', 9, 'bold'), background='#ecf0f1', 
                       foreground='#34495e', relief='flat', padding=3)
        
    def show_year_dialog(self):
        # Create custom centered dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Year")
        dialog.geometry("300x150")
        dialog.configure(bg='#f5f5f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+{}+{}".format(
            int(self.root.winfo_screenwidth()/2 - 150),
            int(self.root.winfo_screenheight()/2 - 75)
        ))
        
        frame = tk.Frame(dialog, bg='#f5f5f5')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(frame, text="Enter Year (1900-2100):", 
                font=('Arial', 12), bg='#f5f5f5').pack(pady=10)
        
        entry = tk.Entry(frame, font=('Arial', 12), justify='center')
        entry.insert(0, str(self.current_year))
        entry.pack(pady=5)
        entry.focus()
        
        def submit():
            try:
                year = int(entry.get())
                if 1900 <= year <= 2100:
                    self.current_year = year
                    dialog.destroy()
                    self.create_calendar()
                else:
                    messagebox.showerror("Error", "Year must be between 1900-2100")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid year")
        
        def on_enter(event):
            submit()
            
        entry.bind('<Return>', on_enter)
        
        btn_frame = tk.Frame(frame, bg='#f5f5f5')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Submit", command=submit, 
                 font=('Arial', 10), bg='#3498db', fg='white',
                 relief='flat', padx=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.root.quit, 
                 font=('Arial', 10), bg='#e74c3c', fg='white',
                 relief='flat', padx=20).pack(side='left', padx=5)
    
    def create_calendar(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.main_frame = tk.Frame(self.root, bg='#f5f5f5')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Create scrollable calendar area
        self.create_scrollable_calendar()
        
        # Create all months instantly
        self.create_all_months()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(header_frame, text=f"Calendar {self.current_year}", 
                              font=('Arial', 24, 'bold'), bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(side='left')
        
        btn_frame = tk.Frame(header_frame, bg='#f5f5f5')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="Change Year", command=self.show_year_dialog,
                 font=('Arial', 10), bg='#3498db', fg='white', relief='flat', padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Today", command=self.go_to_today,
                 font=('Arial', 10), bg='#2ecc71', fg='white', relief='flat', padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Scroll to Top", command=self.scroll_to_top,
                 font=('Arial', 10), bg='#9b59b6', fg='white', relief='flat', padx=15).pack(side='left', padx=5)
    
    def create_scrollable_calendar(self):
        # Create main container frame
        container = tk.Frame(self.main_frame, bg='#f5f5f5')
        container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(container, bg='#f5f5f5', highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(container, orient='horizontal', command=self.canvas.xview)
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Create scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f5f5f5')
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Add scrollable frame to canvas
        canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        # Configure scroll region when frame size changes
        def configure_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            
        def configure_canvas_width(event=None):
            canvas_width = self.canvas.winfo_width()
            self.canvas.itemconfig(canvas_frame, width=canvas_width)
        
        self.scrollable_frame.bind('<Configure>', configure_scroll_region)
        self.canvas.bind('<Configure>', configure_canvas_width)
        
        # Bind mouse wheel scrolling
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        # Bind mousewheel when mouse enters canvas
        self.canvas.bind('<Enter>', bind_mousewheel)
        self.canvas.bind('<Leave>', unbind_mousewheel)
        
        # Also bind arrow keys for keyboard scrolling
        def on_key_press(event):
            if event.keysym == 'Up':
                self.canvas.yview_scroll(-1, "units")
            elif event.keysym == 'Down':
                self.canvas.yview_scroll(1, "units")
            elif event.keysym == 'Left':
                self.canvas.xview_scroll(-1, "units")
            elif event.keysym == 'Right':
                self.canvas.xview_scroll(1, "units")
            elif event.keysym == 'Prior':  # Page Up
                self.canvas.yview_scroll(-10, "units")
            elif event.keysym == 'Next':   # Page Down
                self.canvas.yview_scroll(10, "units")
        
        self.root.bind('<Key>', on_key_press)
        self.root.focus_set()
    
    def create_all_months(self):
        # Create calendar grid container
        cal_frame = tk.Frame(self.scrollable_frame, bg='#f5f5f5')
        cal_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure grid weights for responsive layout
        for i in range(4):  # 4 rows
            cal_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):  # 3 columns
            cal_frame.grid_columnconfigure(i, weight=1)
        
        # Create all 12 months instantly
        for month in range(1, 13):
            row = (month - 1) // 3
            col = (month - 1) % 3
            
            month_frame = self.create_month(cal_frame, month)
            month_frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        
        # Update scroll region after all months are created
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def create_month(self, parent, month_num):
        # Make month frame larger to ensure full visibility
        month_frame = tk.Frame(parent, bg='white', relief='raised', bd=2, 
                              width=280, height=220)
        month_frame.grid_propagate(False)  # Maintain fixed size
        
        # Month header
        header = tk.Label(month_frame, text=calendar.month_name[month_num],
                         font=('Arial', 14, 'bold'), bg='#3498db', fg='white', pady=8)
        header.pack(fill='x')
        
        # Days container with fixed size
        days_frame = tk.Frame(month_frame, bg='white')
        days_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure column weights
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1)
        
        # Day headers
        day_names = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for i, day in enumerate(day_names):
            lbl = tk.Label(days_frame, text=day, font=('Arial', 9, 'bold'),
                          bg='#ecf0f1', fg='#34495e', width=4, height=1)
            lbl.grid(row=0, column=i, sticky='ew', padx=1, pady=1)
        
        # Calendar days
        cal_data = calendar.monthcalendar(self.current_year, month_num)
        for week_num, week in enumerate(cal_data, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(days_frame, text="", width=4, height=2, bg='white')
                else:
                    # Get day styling
                    style_info = self.get_day_style(day, month_num)
                    
                    lbl = tk.Label(days_frame, text=str(day), 
                                  font=style_info['font'],
                                  bg=style_info['bg'], 
                                  fg=style_info['fg'], 
                                  width=4, height=2, relief='solid', bd=1)
                    
                    lbl.bind("<Button-1>", 
                            lambda e, y=self.current_year, m=month_num, d=day: 
                            self.show_date_info(y, m, d))
                
                lbl.grid(row=week_num, column=day_num, sticky='ew', padx=1, pady=1)
            
        return month_frame
    
    def get_day_style(self, day, month_num):
        """Calculate day styling"""
        bg_color = 'white'
        fg_color = 'black'
        font_style = ('Arial', 9)
        
        # Check if weekend
        day_of_week = date(self.current_year, month_num, day).weekday()
        if day_of_week >= 5:  # Weekend
            bg_color = '#ffebee'
            fg_color = '#e74c3c'
        
        # Check if today
        if (self.current_year == self.today.year and 
            month_num == self.today.month and 
            day == self.today.day):
            bg_color = '#2ecc71'
            fg_color = 'white'
            font_style = ('Arial', 9, 'bold')
        
        return {
            'bg': bg_color,
            'fg': fg_color,
            'font': font_style
        }
    
    def show_date_info(self, year, month, day):
        selected_date = date(year, month, day)
        day_name = selected_date.strftime("%A")
        
        info = f"{day_name}, {calendar.month_name[month]} {day}, {year}"
        if selected_date.weekday() >= 5:
            info += "\n(Weekend)"
        if selected_date == self.today:
            info += "\n(Today)"
            
        messagebox.showinfo("Date Info", info)
    
    def go_to_today(self):
        if self.current_year != self.today.year:
            self.current_year = self.today.year
            self.create_calendar()
        else:
            # Scroll to current month
            self.scroll_to_month(self.today.month)
    
    def scroll_to_month(self, month):
        """Scroll to a specific month"""
        # Calculate approximate position of the month
        row = (month - 1) // 3
        # Scroll to approximately that row position
        total_height = self.canvas.bbox('all')[3] if self.canvas.bbox('all') else 1000
        scroll_position = (row / 4.0) * 0.8  # Approximate position
        self.canvas.yview_moveto(scroll_position)
    
    def scroll_to_top(self):
        """Scroll to the top of the calendar"""
        self.canvas.yview_moveto(0)

def main():
    root = tk.Tk()
    
    # Enable full screen on different platforms
    try:
        root.state('zoomed')  # Windows
    except:
        try:
            root.attributes('-zoomed', True)  # Linux
        except:
            root.attributes('-fullscreen', True)  # macOS/fallback
    
    app = CalendarApp(root)
    
    # Bind Escape key to exit fullscreen
    root.bind('<Escape>', lambda e: root.quit())
    
    root.mainloop()

if __name__ == "__main__":
    main()

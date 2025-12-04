import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os

# This is where the student data file is supposed to be
DATA_FILE = r"C:\Users\HP\Desktop\studentMarks.txt"


class DarkMarksApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        # Application title
        self.root.title("Student Manager")
        self.root.geometry("1024x640")
        # Start with my preferred dark mode settings
        self.current_theme = "dark"
        self.root.configure(bg="#0f1724")

        # variables for keeping track of data
        self.records = []  # list of student dictionaries
        self.desc_toggle = False
        self.current_path = None

        # load data and set up UI components
        self._locate_and_load()
        self._style_setup()
        self._build_ui()
        self._apply_theme("dark") # make sure the colors are right when starting
        self.show_list_view()
        self._set_status("Ready")

    # --- File Handlers ---
    def _locate_and_load(self):
        # try to find the data file and load it
        path = self._find_data_file()
        if path:
            self.current_path = path
            self._load_from_file(path)

    def _find_data_file(self):
        # check the default path first
        if os.path.exists(DATA_FILE):
            return DATA_FILE
        # if not there, check the script's directory
        try:
            local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")
            if os.path.exists(local):
                return local
        except Exception:
            pass

        # if all else fails, ask the user to find it
        messagebox.showwarning("File not found",
                               "Couldn't find studentMarks.txt. Gotta select it manually.")
        chosen = filedialog.askopenfilename(
            title="Select studentMarks.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        return chosen or None

    def _load_from_file(self, path):
        self.records.clear()
        bad = 0 # counter for corrupted lines
        try:
            with open(path, "r") as f:
                content = f.readlines()
            if not content:
                return
            
            # handle the optional student count line at the top
            try:
                count = int(content[0].strip())
                lines = content[1:1+count]
            except Exception:
                lines = content

            for ln in lines:
                ln = ln.strip()
                if not ln:
                    continue
                parts = ln.split(",")
                if len(parts) != 6:
                    bad += 1
                    continue
                code, name, a, b, c, exam = parts
                try:
                    # convert strings to the right types
                    rec = {
                        "code": code.strip(),
                        "name": name.strip(),
                        "cw1": int(a),
                        "cw2": int(b),
                        "cw3": int(c),
                        "exam": int(exam)
                    }
                except ValueError:
                    bad += 1 # not a number, skip this line
                    continue
                self.records.append(rec)
            
            if bad:
                messagebox.showwarning("Data Warning", f"{bad} lines looked wrong and were ignored.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Uh oh, couldn't read the file:\n{e}")

    def _save_to_file(self):
        # save the current records back to the file
        path = self.current_path
        if not path:
            messagebox.showerror("Save Error", "Can't save, no file was selected.")
            return
        try:
            with open(path, "w") as f:
                # write the number of records first
                f.write(str(len(self.records)) + "\n")
                # write each record as a comma-separated line
                for r in self.records:
                    line = f"{r['code']},{r['name']},{r['cw1']},{r['cw2']},{r['cw3']},{r['exam']}\n"
                    f.write(line)
            self._set_status("Saved changes.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Something went wrong saving the file:\n{e}")

    # --- Calculations ---
    def _cw_total(self, r):
        # calculate total coursework score (out of 60)
        return r["cw1"] + r["cw2"] + r["cw3"]

    def _overall_pct(self, r):
        # calculate overall percentage (total / 160)
        total = self._cw_total(r) + r["exam"]
        return round((total / 160) * 100, 2)

    def _grade_from_pct(self, pct):
        # simple grading logic based on percentage
        if pct >= 70:
            return "A"
        if pct >= 60:
            return "B"
        if pct >= 50:
            return "C"
        if pct >= 40:
            return "D"
        return "F"

    # --- UI Styling and Theme Toggling ---
    def _style_setup(self):
        style = ttk.Style()
        style.theme_use("clam") # base theme

        # --- DARK THEME STYLES (My default look) ---
        style.configure("Dark.Treeview",
                        background="#0b1220",
                        foreground="#e6eef6",
                        fieldbackground="#0b1220",
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Dark.Treeview.Heading",
                        background="#0b1220",
                        foreground="#e6eef6",
                        font=("Segoe UI", 10, "bold"))
        style.map("Dark.Treeview.Heading",
                  background=[("active", "#20324a")])

        style.configure("Dark.Side.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        foreground="#eaf2ff",
                        background="#0b3b66")
        style.map("Dark.Side.TButton", background=[("active", "#064e7a")])

        style.configure("Dark.Header.TLabel",
                        font=("Segoe UI", 16, "bold"),
                        foreground="#eaf2ff",
                        background="#0f1724")
        style.configure("Dark.Sub.TLabel",
                        font=("Segoe UI", 10),
                        foreground="#9fb0c8",
                        background="#0f1724")
        
        # --- BRIGHT THEME STYLES (for light mode) ---
        style.configure("Bright.Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        fieldbackground="#ffffff",
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Bright.Treeview.Heading",
                        background="#e0e0e0",
                        foreground="#000000",
                        font=("Segoe UI", 10, "bold"))
        style.map("Bright.Treeview.Heading",
                  background=[("active", "#cccccc")])
        
        style.configure("Bright.Side.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        foreground="#000000",
                        background="#cccccc")
        style.map("Bright.Side.TButton", background=[("active", "#aaaaaa")])
        
        style.configure("Bright.Header.TLabel",
                        font=("Segoe UI", 16, "bold"),
                        foreground="#000000",
                        background="#f0f0f0")
        style.configure("Bright.Sub.TLabel",
                        font=("Segoe UI", 10),
                        foreground="#666666",
                        background="#f0f0f0")

    def _apply_theme(self, theme):
        # this function changes all colors at once
        if theme == "dark":
            # set all the dark colors
            self.root.configure(bg="#0f1724")
            self.sidebar.configure(bg="#06202e")
            self.main.configure(bg="#0f1724")
            for w in self.sidebar.winfo_children():
                 if isinstance(w, tk.Label):
                    w.configure(bg="#06202e", fg="#eaf2ff" if w["text"] != "📘" else "#cfe8ff")
            self.status.configure(bg="#071426", fg="#b9d6ef")
            # save the active style names
            self.tree_style = "Dark.Treeview"
            self.header_style = "Dark.Header.TLabel"
            self.sub_style = "Dark.Sub.TLabel"
            self.main_bg = "#0f1724"
            self.status_fg = "#b9d6ef"
            self.current_theme = "dark"
            self.theme_btn.configure(text="💡 Bright Mode")
        else: # bright mode
            # set all the bright colors
            self.root.configure(bg="#f0f0f0")
            self.sidebar.configure(bg="#dddddd")
            self.main.configure(bg="#f0f0f0")
            for w in self.sidebar.winfo_children():
                if isinstance(w, tk.Label):
                    w.configure(bg="#dddddd", fg="#000000" if w["text"] != "📘" else "#000000")
            self.status.configure(bg="#cccccc", fg="#333333")
            # save the active style names
            self.tree_style = "Bright.Treeview"
            self.header_style = "Bright.Header.TLabel"
            self.sub_style = "Bright.Sub.TLabel"
            self.main_bg = "#f0f0f0"
            self.status_fg = "#333333"
            self.current_theme = "bright"
            self.theme_btn.configure(text="🌙 Dark Mode")
        
        # force the list view to reload with the new colors
        if hasattr(self, 'tree'):
             self.show_list_view()

    def _toggle_theme(self):
        # simply switch between the two themes
        new_theme = "bright" if self.current_theme == "dark" else "dark"
        self._apply_theme(new_theme)


    def _build_ui(self):
        # setup the left sidebar panel
        self.sidebar = tk.Frame(self.root, width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="📘", font=("Segoe UI Emoji", 28)).pack(pady=10)
        # CHANGED: Updated the label text to match the new application title
        tk.Label(self.sidebar, text="Student Manager", font=("Segoe UI", 12, "bold")).pack()
        
        # button to switch themes
        self.theme_btn = ttk.Button(self.sidebar, text="💡 Bright Mode", style="Dark.Side.TButton", command=self._toggle_theme)
        self.theme_btn.pack(fill="x", padx=14, pady=(10, 16))

        # list of buttons for the sidebar functionality
        btn_specs = [
            ("List all", self.show_list_view),
            ("Find", self._search_dialog),
            ("Highest", self._show_extreme_max),
            ("Lowest", self._show_extreme_min),
            ("Sort", self._sort_dialog),
            ("Add", self._add_view),
            ("Edit (select row)", self._edit_selected),
            ("Delete (select row)", self._delete_selected),
        ]
        for txt, cmd in btn_specs:
            b = ttk.Button(self.sidebar, text=txt, style="Dark.Side.TButton", command=cmd)
            b.pack(fill="x", padx=14, pady=6)

        # main area for tables and forms
        self.main = tk.Frame(self.root)
        self.main.pack(side="right", fill="both", expand=True)

        # status bar at the bottom
        self.status_var = tk.StringVar()
        self.status = tk.Label(self.root, textvariable=self.status_var, anchor="w", padx=10)
        self.status.pack(side="bottom", fill="x")
        
        # initialize placeholders for theme colors
        self.tree_style = ""
        self.header_style = ""
        self.sub_style = ""
        self.main_bg = ""
        self.status_fg = ""
        
        self._apply_theme("dark") # set up initial colors

    def _set_status(self, txt):
        # update the message in the status bar
        self.status_var.set(txt)

    def _clear_main(self):
        # remove all widgets from the main content area
        for w in self.main.winfo_children():
            w.destroy()

    # --- List/Table View (The main screen) ---
    def show_list_view(self):
        self._clear_main()
        hdr = ttk.Label(self.main, text="All Students", style=self.header_style)
        hdr.pack(anchor="w", padx=18, pady=(14, 6))

        sub = ttk.Label(self.main, text="CW (3x20), Exam (100). Double-click for details.",
                        style=self.sub_style)
        sub.pack(anchor="w", padx=18, pady=(0, 8))

        # container for the Treeview widget
        container = tk.Frame(self.main, bg="#111111" if self.current_theme == "dark" else "#eeeeee") 
        container.pack(fill="both", expand=True, padx=16, pady=12)

        cols = ("code", "name", "cw_total", "exam", "pct", "grade")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", style=self.tree_style)

        # setup column headers and commands for sorting
        self.tree.heading("code", text="Code", command=lambda: self._sort_by("code"))
        self.tree.heading("name", text="Name", command=lambda: self._sort_by("name"))
        self.tree.heading("cw_total", text="Coursework", command=lambda: self._sort_by("cw_total"))
        self.tree.heading("exam", text="Exam", command=lambda: self._sort_by("exam"))
        self.tree.heading("pct", text="Overall %", command=lambda: self._sort_by("pct"))
        self.tree.heading("grade", text="Grade", command=lambda: self._sort_by("grade"))

        # set column widths and alignment
        self.tree.column("code", width=80, anchor="center")
        self.tree.column("name", width=260, anchor="w")
        self.tree.column("cw_total", width=110, anchor="center")
        self.tree.column("exam", width=100, anchor="center")
        self.tree.column("pct", width=110, anchor="center")
        self.tree.column("grade", width=80, anchor="center")

        # add a scrollbar
        vs = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vs.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vs.pack(side="right", fill="y")

        # alternating row colors and grade-specific colors
        if self.current_theme == "dark":
            self.tree.tag_configure("odd", background="#07263a")
            self.tree.tag_configure("even", background="#041723")
        else: 
            self.tree.tag_configure("odd", background="#f5f5f5")
            self.tree.tag_configure("even", background="#ffffff")
            
        # Grade colors (make them look okay in both themes)
        self.tree.tag_configure("A", foreground="#008800" if self.current_theme == "bright" else "#7ef0a6")
        self.tree.tag_configure("B", foreground="#33aa33" if self.current_theme == "bright" else "#8fe6a8")
        self.tree.tag_configure("C", foreground="#cc9900" if self.current_theme == "bright" else "#ffd27a")
        self.tree.tag_configure("D", foreground="#cc6600" if self.current_theme == "bright" else "#ffb27a")
        self.tree.tag_configure("F", foreground="#cc0000" if self.current_theme == "bright" else "#ff8a8a")

        self._populate_tree()
        self.tree.bind("<Double-1>", self._on_row_double) # double-click for detail view

        # display a summary of the class average
        summary = tk.Label(self.main, text=self._class_summary(), bg=self.main_bg, fg=self.status_fg, anchor="w",
                             font=("Segoe UI", 10))
        summary.pack(fill="x", padx=18, pady=(10, 20))
        self._set_status("Showing all students")
    
    def _populate_tree(self):
        # fill the Treeview with data from self.records
        if not hasattr(self, "tree"):
            return
        # clear existing data
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        for i, rec in enumerate(self.records):
            cw = self._cw_total(rec)
            pct = self._overall_pct(rec)
            grd = self._grade_from_pct(pct)
            tag_row = "odd" if i % 2 == 0 else "even"
            # insert the row with calculated values and color tags
            self.tree.insert("", "end", values=(rec["code"], rec["name"], cw, rec["exam"], f"{pct}%", grd),
                             tags=(tag_row, grd))

    def _class_summary(self):
        # calculate the class average percentage
        if not self.records:
            return "No students."
        total = sum(self._overall_pct(r) for r in self.records)
        avg = round(total / len(self.records), 2)
        return f"Students: {len(self.records)}    |    Average %: {avg}"

    def _on_row_double(self, event):
        # handler for double-clicking a row
        sel = self.tree.selection()
        if not sel:
            return
        code = self.tree.item(sel[0], "values")[0]
        rec = self._by_code(code)
        if rec:
            self._detail_view(rec)

    # --- Detail / Edit / Delete ---
    def _detail_view(self, rec):
        self._clear_main()
        hdr = ttk.Label(self.main, text=f"{rec['name']}  ({rec['code']})", style=self.header_style)
        hdr.pack(anchor="w", padx=18, pady=(14, 6))

        # set up colors based on active theme
        frame_bg = "#08182a" if self.current_theme == "dark" else "#e9e9e9"
        text_fg = "#dff1ff" if self.current_theme == "dark" else "#000000"
        value_fg = "#cfe8ff" if self.current_theme == "dark" else "#333333"
        
        frame = tk.Frame(self.main, bg=frame_bg, padx=16, pady=16)
        frame.pack(fill="x", padx=18, pady=12)

        def row(label, value):
            # helper to create a label: value row
            r = tk.Frame(frame, bg=frame_bg)
            r.pack(anchor="w", pady=6, fill="x")
            tk.Label(r, text=f"{label}:", bg=frame_bg, fg=text_fg, font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(r, text=value, bg=frame_bg, fg=value_fg, font=("Segoe UI", 10)).pack(side="left", padx=8)

        # display all the student's details and calculated results
        row("Coursework marks", f"{rec['cw1']}, {rec['cw2']}, {rec['cw3']}")
        row("Coursework total", f"{self._cw_total(rec)} / 60")
        row("Exam", f"{rec['exam']} / 100")
        pct = self._overall_pct(rec)
        row("Overall %", f"{pct}%")
        row("Grade", self._grade_from_pct(pct))

        # action buttons
        btns = tk.Frame(self.main, bg=self.main_bg)
        btns.pack(fill="x", padx=18, pady=(6, 12))
        
        # custom button colors
        edit_bg = "#0b5a8a" if self.current_theme == "dark" else "#007bff"
        delete_bg = "#a82b2b" if self.current_theme == "dark" else "#dc3545"
        back_bg = "#334c63" if self.current_theme == "dark" else "#6c757d"
        btn_fg = "white"

        tk.Button(btns, text="Edit", bg=edit_bg, fg=btn_fg, relief="flat", padx=10, pady=6,
                     command=lambda: self._open_edit_window(rec)).pack(side="left", padx=6)
        tk.Button(btns, text="Delete", bg=delete_bg, fg=btn_fg, relief="flat", padx=10, pady=6,
                     command=lambda: self._confirm_delete(rec)).pack(side="left", padx=6)
        tk.Button(btns, text="Back", bg=back_bg, fg=btn_fg, relief="flat", padx=10, pady=6,
                     command=self.show_list_view).pack(side="left", padx=6)
        self._set_status(f"Viewing {rec['name']}")

    def _confirm_delete(self, rec):
        # confirmation before deleting a record
        if messagebox.askyesno("Confirm Delete", f"You sure you wanna delete {rec['name']} ({rec['code']})?"):
            try:
                self.records.remove(rec)
                self._save_to_file()
                self.show_list_view()
                self._set_status(f"Deleted {rec['name']}")
            except Exception as e:
                messagebox.showerror("Delete Error", str(e))

    def _open_edit_window(self, rec):
        # Toplevel window for editing marks
        win = tk.Toplevel(self.root)
        win.title("Edit marks")
        
        win_bg = "#061328" if self.current_theme == "dark" else "#f8f9fa"
        win_fg = "#dff1ff" if self.current_theme == "dark" else "#343a40"
        btn_bg = "#1b7ca6" if self.current_theme == "dark" else "#28a745"
        
        win.configure(bg=win_bg)
        fields = [("Coursework 1", "cw1"), ("Coursework 2", "cw2"), ("Coursework 3", "cw3"), ("Exam", "exam")]
        entries = {}
        # create input fields for each mark
        for i, (lab, key) in enumerate(fields):
            tk.Label(win, text=lab + ":", bg=win_bg, fg=win_fg).grid(row=i, column=0, sticky="w", padx=10, pady=6)
            e = tk.Entry(win)
            e.grid(row=i, column=1, padx=10, pady=6, sticky="ew")
            e.insert(0, str(rec[key]))
            entries[key] = e
        win.grid_columnconfigure(1, weight=1)

        def apply():
            # validate inputs and save changes
            try:
                c1 = int(entries["cw1"].get()); c2 = int(entries["cw2"].get()); c3 = int(entries["cw3"].get()); ex = int(entries["exam"].get())
                # validate ranges
                for v in (c1, c2, c3):
                    if not (0 <= v <= 20): raise ValueError("Coursework has to be between 0 and 20!")
                if not (0 <= ex <= 100): raise ValueError("Exam has to be between 0 and 100!")
                    
                # update the record and save
                rec["cw1"], rec["cw2"], rec["cw3"], rec["exam"] = c1, c2, c3, ex
                self._save_to_file()
                win.destroy()
                self.show_list_view()
                self._set_status(f"Updated {rec['name']}")
            except ValueError as ve:
                messagebox.showerror("Invalid", str(ve))

        tk.Button(win, text="Save", bg=btn_bg, fg="white", command=apply, padx=10, pady=6).grid(row=len(fields), column=0, columnspan=2, pady=10)

    # --- Add / Find / Sort ---
    def _add_view(self):
        # screen for adding a new student record
        self._clear_main()
        ttk.Label(self.main, text="Add Student", style=self.header_style).pack(anchor="w", padx=18, pady=(14, 6))
        
        frm_bg = "#071426" if self.current_theme == "dark" else "#ffffff"
        frm_fg = "#dff1ff" if self.current_theme == "dark" else "#343a40"
        btn_bg = "#1b7ca6" if self.current_theme == "dark" else "#28a745"
        
        frm = tk.Frame(self.main, bg=frm_bg, padx=14, pady=14)
        frm.pack(fill="x", padx=18, pady=12)

        labels = [("Code", "code"), ("Name", "name"), ("CW1", "cw1"), ("CW2", "cw2"), ("CW3", "cw3"), ("Exam", "exam")]
        entries = {}
        # create input fields for all required data
        for i, (lab, key) in enumerate(labels):
            tk.Label(frm, text=lab + ":", bg=frm_bg, fg=frm_fg).grid(row=i, column=0, sticky="w", pady=6)
            e = tk.Entry(frm)
            e.grid(row=i, column=1, sticky="ew", padx=(8, 0), pady=6)
            entries[key] = e
        frm.grid_columnconfigure(1, weight=1)

        def save_new():
            # grab and validate all new student data
            try:
                code = entries["code"].get().strip()
                name = entries["name"].get().strip()
                if not code or not name:
                    raise ValueError("Fill in the code and name!")
                if not (code.isdigit() and 1000 <= int(code) <= 9999):
                    raise ValueError("Code must be a 4-digit number (1000-9999)")
                
                # convert marks to integers and check range
                cw1 = int(entries["cw1"].get()); cw2 = int(entries["cw2"].get()); cw3 = int(entries["cw3"].get()); ex = int(entries["exam"].get())
                for v in (cw1, cw2, cw3):
                    if not (0 <= v <= 20): raise ValueError("CW must be 0-20")
                if not (0 <= ex <= 100): raise ValueError("Exam must be 0-100")
                
                # check for duplicate student code
                if any(r["code"] == code for r in self.records):
                    raise ValueError("A student with this code already exists")
                    
                # create, add, and save the new record
                rec = {"code": code, "name": name, "cw1": cw1, "cw2": cw2, "cw3": cw3, "exam": ex}
                self.records.append(rec)
                self._save_to_file()
                self.show_list_view()
                self._set_status(f"Added {name}")
            except ValueError as ve:
                messagebox.showerror("Invalid input", str(ve))

        tk.Button(self.main, text="Create", bg=btn_bg, fg="white", command=save_new, padx=12, pady=8).pack(anchor="e", padx=18, pady=(6, 12))

    def _by_code(self, code):
        # find a record by student code
        for r in self.records:
            if str(r["code"]) == str(code):
                return r
        return None

    def _edit_selected(self):
        # wrapper to open edit window for the selected row
        if not hasattr(self, "tree"):
            messagebox.showinfo("Select", "Open the list view and select a row to edit.")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Gotta select a row first!")
            return
        code = self.tree.item(sel[0], "values")[0]
        rec = self._by_code(code)
        if rec:
            self._open_edit_window(rec)

    def _delete_selected(self):
        # wrapper to confirm and delete the selected row
        if not hasattr(self, "tree"):
            messagebox.showinfo("Select", "Open the list view and select a row to delete.")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Gotta select a row first!")
            return
        code = self.tree.item(sel[0], "values")[0]
        rec = self._by_code(code)
        if rec:
            self._confirm_delete(rec)

    def _search_dialog(self):
        # search by code or name
        if not self.records:
            messagebox.showinfo("No data", "No students to search through.")
            return
        q = simpledialog.askstring("Search", "Enter student code or full name:")
        if not q:
            return
        q = q.strip()
        # check code match
        rec = self._by_code(q)
        if rec:
            self._detail_view(rec); return
        # check exact name match
        for r in self.records:
            if r["name"].lower() == q.lower():
                self._detail_view(r); return
        # check partial name match
        matches = [r for r in self.records if q.lower() in r["name"].lower()]
        if not matches:
            messagebox.showinfo("Not found", "Nobody matched that query.")
        elif len(matches) == 1:
            self._detail_view(matches[0])
        else:
            # show multiple matches if more than one found
            msg = "\n".join(f"{m['name']} ({m['code']})" for m in matches)
            messagebox.showinfo("Multiple matches", msg)

    def _show_extreme_max(self):
        # find and show the student with the highest overall percentage
        if not self.records:
            messagebox.showinfo("No data", "No students available.")
            return
        rec = max(self.records, key=self._overall_pct)
        self._detail_view(rec)

    def _show_extreme_min(self):
        # find and show the student with the lowest overall percentage
        if not self.records:
            messagebox.showinfo("No data", "No students available.")
            return
        rec = min(self.records, key=self._overall_pct)
        self._detail_view(rec)

    def _sort_dialog(self):
        # dialogue window to sort by percentage (asc/desc)
        if not self.records:
            messagebox.showinfo("No data", "No students to sort.")
            return
        win = tk.Toplevel(self.root)
        win.title("Sort by")
        
        win_bg = "#081a2a" if self.current_theme == "dark" else "#f8f9fa"
        win_fg = "#dff1ff" if self.current_theme == "dark" else "#343a40"
        btn_bg = "#1b7ca6" if self.current_theme == "dark" else "#007bff"
        radio_fg = "#e0f2ff" if self.current_theme == "dark" else "#000000"
        
        win.configure(bg=win_bg)
        tk.Label(win, text="Sort by overall percentage:", bg=win_bg, fg=win_fg).pack(padx=12, pady=(12, 6))
        var = tk.StringVar(value="asc")
        tk.Radiobutton(win, text="Ascending", variable=var, value="asc", bg=win_bg, fg=radio_fg).pack(anchor="w", padx=12)
        tk.Radiobutton(win, text="Descending", variable=var, value="desc", bg=win_bg, fg=radio_fg).pack(anchor="w", padx=12)

        def apply_sort():
            # sort the list and update the display
            reverse = (var.get() == "desc")
            self.records.sort(key=self._overall_pct, reverse=reverse)
            self._save_to_file()
            self.show_list_view()
            win.destroy()
            self._set_status("Sorted records")

        tk.Button(win, text="Apply", bg=btn_bg, fg="white", command=apply_sort).pack(pady=10, padx=12)

    # --- Utility Functions (for column header sorting) ---
    def _sort_by(self, key):
        # dynamic sorting function for Treeview column headers
        if not self.records:
            return
        # select the correct function to get the value for sorting
        if key == "code":
            func = lambda r: int(r["code"])
        elif key == "name":
            func = lambda r: r["name"].lower()
        elif key == "cw_total":
            func = lambda r: self._cw_total(r)
        elif key == "exam":
            func = lambda r: r["exam"]
        elif key == "pct":
            func = lambda r: self._overall_pct(r)
        elif key == "grade":
            # sort by grade (A, B, C...)
            func = lambda r: self._grade_from_pct(self._overall_pct(r))
        else:
            return
            
        # toggle between ascending and descending
        self.desc_toggle = not getattr(self, "desc_toggle", False)
        self.records.sort(key=func, reverse=self.desc_toggle)
        
        if hasattr(self, "tree"):
            self._populate_tree()
        self._set_status(f"Sorted by {key} ({'desc' if self.desc_toggle else 'asc'})")

# --- Main Execution ---
def main():
    root = tk.Tk()
    app = DarkMarksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
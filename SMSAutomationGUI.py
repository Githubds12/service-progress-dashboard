import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import threading
import time

# --- Configuration ---
IP = "62.238.2.204"
ACCESS_PORT = "3666"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
DB_FILE = r"C:\Users\Gorri\Documents\Reports\operator_database_clean.json"
MASTER_DB_FILE = r"C:\HTB-Notes-Portal\full_live_operators_db.json"

ACCESS_INFO_URL = f"http://{IP}:{ACCESS_PORT}/accessinfo"
BASE_URL = f"http://{IP}:{API_PORT}/api"

# --- Dial Code Mapping ---
COUNTRY_DIAL_CODES = {
    "AF": "+93", "AL": "+355", "DZ": "+213", "AD": "+376", "AO": "+244", "AR": "+54", "AM": "+374", "AU": "+61", "AT": "+43", "AZ": "+994",
    "BH": "+973", "BD": "+880", "BY": "+375", "BE": "+32", "BO": "+591", "BA": "+387", "BR": "+55", "BG": "+359", "KH": "+855", "CM": "+237",
    "CA": "+1", "CL": "+56", "CN": "+86", "CO": "+57", "CR": "+506", "HR": "+385", "CU": "+53", "CY": "+357", "CZ": "+420", "DK": "+45",
    "DO": "+1", "EC": "+593", "EG": "+20", "SV": "+503", "EE": "+372", "ET": "+251", "FI": "+358", "FR": "+33", "GE": "+995", "DE": "+49",
    "GH": "+233", "GR": "+30", "GT": "+502", "HT": "+509", "HN": "+504", "HK": "+852", "HU": "+36", "IS": "+354", "IN": "+91", "ID": "+62",
    "IR": "+98", "IQ": "+964", "IE": "+353", "IL": "+972", "IT": "+39", "JM": "+1", "JP": "+81", "JO": "+962", "KZ": "+7", "KE": "+254",
    "KW": "+965", "KG": "+996", "LV": "+371", "LB": "+961", "LY": "+218", "LT": "+370", "LU": "+352", "MY": "+60", "ML": "+223", "MT": "+356",
    "MX": "+52", "MD": "+373", "MC": "+377", "MN": "+976", "ME": "+382", "MA": "+212", "MZ": "+258", "MM": "+95", "NP": "+977", "NL": "+31",
    "NZ": "+64", "NI": "+505", "NG": "+234", "MK": "+389", "NO": "+47", "OM": "+968", "PK": "+92", "PS": "+970", "PA": "+507", "PY": "+595",
    "PE": "+51", "PH": "+63", "PL": "+48", "PT": "+351", "QA": "+974", "RO": "+40", "RU": "+7", "SA": "+966", "SN": "+221", "RS": "+381",
    "SG": "+65", "SK": "+421", "SI": "+386", "ZA": "+27", "KR": "+82", "ES": "+34", "LK": "+94", "SD": "+249", "SE": "+46", "CH": "+41",
    "SY": "+963", "TW": "+886", "TJ": "+992", "TZ": "+255", "TH": "+66", "TN": "+216", "TR": "+90", "TM": "+993", "UG": "+256", "UA": "+380",
    "US": "+1", "UY": "+598", "UZ": "+998", "VE": "+58", "VN": "+84", "YE": "+967", "ZM": "+260", "ZW": "+263"
}

# --- High Success Operators ---
HIGH_SUCCESS_OPERATORS = {
    "IT": ["fastweb", "windtre", "special", "iliad", "spusu", "tim"]
}

class SMSAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Pulse - SMS Automation")
        self.root.geometry("800x700")
        self.root.configure(bg="#0f172a")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#6366f1")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#4f46e5", foreground="white", borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#6366f1")])
        self.style.configure("TNotebook", background="#0f172a", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1e293b", foreground="#f8fafc", padding=[15, 5], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#4f46e5")])
        
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", pady=10, padx=20)
        ttk.Label(title_frame, text="SMS Automation Portal", style="Header.TLabel").pack(side="left")
        
        self.setup_action_panel()
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tabs
        self.tab_country = ttk.Frame(self.notebook)
        self.tab_live = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_country, text="Master Country DB")
        self.notebook.add(self.tab_live, text="Live Service Search")
        self.notebook.add(self.tab_history, text="History Logs")
        
        self.setup_country_tab()
        self.setup_live_tab()
        self.setup_history_tab()
        
        self.selected_country = None
        self.selected_operator = None
        self.current_number = None
        self.history_items = {}

    def setup_live_tab(self):
        top = ttk.Frame(self.tab_live)
        top.pack(fill="x", pady=15, padx=15)
        
        ttk.Label(top, text="Service Name:").pack(side="left", padx=(0, 10))
        self.service_entry = ttk.Entry(top, width=30, font=("Segoe UI", 10))
        self.service_entry.pack(side="left", padx=10)
        self.service_entry.bind("<Return>", lambda e: self.search_live())
        
        btn = ttk.Button(top, text="Search Live", command=self.search_live)
        btn.pack(side="left", padx=10)
        
        self.tree_live = self.create_treeview(self.tab_live)
        self.tree_live.bind("<<TreeviewSelect>>", self.on_tree_select)

    def setup_country_tab(self):
        top = ttk.Frame(self.tab_country)
        top.pack(fill="x", pady=15, padx=15)
        
        ttk.Label(top, text="Country Code / Name:").pack(side="left", padx=(0, 10))
        self.country_entry = ttk.Entry(top, width=30, font=("Segoe UI", 10))
        self.country_entry.pack(side="left", padx=10)
        self.country_entry.bind("<Return>", lambda e: self.search_country())
        
        btn = ttk.Button(top, text="Search Master DB", command=self.search_country)
        btn.pack(side="left", padx=10)
        
        self.tree_country = self.create_treeview(self.tab_country)
        self.tree_country.bind("<<TreeviewSelect>>", self.on_tree_select)

    def create_treeview(self, parent):
        columns = ("ccode", "country", "operator", "count", "high_success")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        tree.heading("ccode", text="Code")
        tree.column("ccode", width=60, anchor="center")
        tree.heading("country", text="Country")
        tree.column("country", width=150)
        tree.heading("operator", text="Operator")
        tree.column("operator", width=150)
        tree.heading("count", text="Available")
        tree.column("count", width=80, anchor="center")
        tree.heading("high_success", text="Rating")
        tree.column("high_success", width=120)
        
        tree.tag_configure("high", foreground="#10b981", font=("Segoe UI", 10, "bold"))
        tree.pack(fill="both", expand=True, padx=15, pady=5)
        return tree

    def setup_history_tab(self):
        columns = ("time", "number", "operator", "message")
        self.tree_history = ttk.Treeview(self.tab_history, columns=columns, show="headings", height=15)
        self.tree_history.heading("time", text="Time")
        self.tree_history.column("time", width=80, anchor="center")
        self.tree_history.heading("number", text="Number")
        self.tree_history.column("number", width=130, anchor="center")
        self.tree_history.heading("operator", text="Operator")
        self.tree_history.column("operator", width=120, anchor="center")
        self.tree_history.heading("message", text="Status / SMS Message")
        self.tree_history.column("message", width=400)
        
        self.tree_history.tag_configure("arrived", foreground="#10b981", font=("Segoe UI", 10, "bold"))
        self.tree_history.pack(fill="both", expand=True, padx=15, pady=15)

    def setup_action_panel(self):
        panel = tk.Frame(self.root, bg="#1e293b", bd=1, relief="ridge")
        panel.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.lbl_selected = tk.Label(panel, text="No operator selected", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 11, "bold"))
        self.lbl_selected.pack(pady=(15, 5))
        
        button_frame = tk.Frame(panel, bg="#1e293b")
        button_frame.pack(pady=5)
        
        self.btn_get_number = ttk.Button(button_frame, text="Get Number", command=self.get_number, state="disabled")
        self.btn_get_number.pack(side="left", padx=5)
        
        self.btn_test_sms = ttk.Button(button_frame, text="Send Test SMS", command=self.send_test_sms, state="disabled")
        self.btn_test_sms.pack(side="left", padx=5)
        
        self.btn_refresh_sms = ttk.Button(button_frame, text="Refresh SMS", command=self.refresh_sms, state="disabled")
        self.btn_refresh_sms.pack(side="left", padx=5)
        
        self.lbl_number = tk.Label(panel, text="", bg="#1e293b", fg="#10b981", font=("Segoe UI", 18, "bold"))
        self.lbl_number.pack(pady=5)
        
        self.lbl_sms = tk.Label(panel, text="", bg="#1e293b", fg="#f59e0b", font=("Segoe UI", 12))
        self.lbl_sms.pack(pady=5)

        output_frame = tk.Frame(panel, bg="#0f172a", bd=1, relief="sunken")
        output_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(output_frame, text="Raw API Output Logs:", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 9)).pack(anchor="w", padx=5, pady=(5,0))

        self.txt_output = tk.Text(output_frame, height=4, bg="#0f172a", fg="#a5b4fc", font=("Consolas", 10), wrap="word", state="disabled", bd=0)
        self.txt_output.pack(fill="x", padx=5, pady=5)

    def update_raw_output(self, text):
        self.txt_output.config(state="normal")
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, text)
        self.txt_output.config(state="disabled")

    def on_tree_select(self, event):
        tree = event.widget
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = item['values']
            self.selected_country = values[0]
            
            # Clean up visual stars for the actual API request
            raw_op = str(values[2]).replace("*** ", "").replace(" ***", "").strip().lower()
            self.selected_operator = raw_op
            
            self.lbl_selected.config(text=f"Selected: {self.selected_country} - {self.selected_operator}", fg="#f8fafc")
            self.btn_get_number.config(state="normal")

    def search_live(self):
        service = self.service_entry.get().strip().lower()
        if not service: return
        
        for item in self.tree_live.get_children():
            self.tree_live.delete(item)
            
        def fetch():
            try:
                res = requests.get(ACCESS_INFO_URL, params={"interval": "10min", "service": service, "token": TOKEN}, timeout=15)
                data = res.json()
                if data.get("status") == "Data retrieved successfully" and data.get("data"):
                    for item in data["data"]:
                        raw_ccode = item.get("ccode")
                        raw_op = item.get("operator")
                        
                        ccode = raw_ccode.upper() if raw_ccode else "UNKNOWN"
                        op = raw_op.lower() if raw_op else "unknown"
                        
                        is_high = ccode in HIGH_SUCCESS_OPERATORS and op in HIGH_SUCCESS_OPERATORS[ccode]
                        display_op = f"*** {op.upper()} ***" if is_high else op
                        rating = "BEST RATE" if is_high else ""
                        tag = "high" if is_high else ""
                        
                        country_name = item.get("country") or "Unknown"
                        self.tree_live.insert("", "end", values=(ccode, country_name, display_op, item.get("access_count", 0), rating), tags=(tag,))
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        threading.Thread(target=fetch, daemon=True).start()

    def search_country(self):
        query = self.country_entry.get().strip().upper()
        if not query: return
        
        for item in self.tree_country.get_children():
            self.tree_country.delete(item)
            
        if not os.path.exists(MASTER_DB_FILE):
            messagebox.showerror("Error", "Master DB not found!")
            return
            
        with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        matched_ccode = None
        for ccode, details in db.items():
            country_name = details.get('country_name')
            country_upper = country_name.upper() if country_name else ""
            
            # Check ISO Code, Country Name, or Dial Code
            dial_code = COUNTRY_DIAL_CODES.get(ccode, "").replace("+", "")
            if query == ccode or query == country_upper or query == dial_code:
                matched_ccode = ccode
                break
                
        if matched_ccode:
            ops = db[matched_ccode]['operators']
            for op in ops:
                is_high = matched_ccode in HIGH_SUCCESS_OPERATORS and op.lower() in HIGH_SUCCESS_OPERATORS[matched_ccode]
                display_op = f"*** {op.upper()} ***" if is_high else op
                rating = "BEST RATE" if is_high else ""
                tag = "high" if is_high else ""
                
                self.tree_country.insert("", "end", values=(matched_ccode, db[matched_ccode]['country_name'], display_op, "Cached", rating), tags=(tag,))
        else:
            messagebox.showinfo("Not Found", f"Search '{query}' not found in DB.\n\nTry ISO codes (IN, TR) or Country Names (INDIA).")

    def get_number(self):
        if not self.selected_country or not self.selected_operator:
            return
            
        self.btn_get_number.config(state="disabled")
        self.lbl_number.config(text="Fetching number...", fg="#f59e0b")
        self.lbl_sms.config(text="")
        
        def fetch():
            safe_op = self.selected_operator.replace("ü", "u").replace("ö", "o")
            params = {"country": self.selected_country, "operator": safe_op, "count": 1, "token": TOKEN}
            try:
                res = requests.get(f"{BASE_URL}/get_numbers", params=params, timeout=15)
                data = res.json()
                if data.get("success") and data.get("number"):
                    raw_num = data["number"][0]
                    self.current_number = raw_num
                    
                    # Format with separated country dial code
                    dial_code = COUNTRY_DIAL_CODES.get(self.selected_country.upper(), "")
                    clean_dial = dial_code.replace("+", "")
                    
                    display_num = raw_num
                    if clean_dial and raw_num.startswith(clean_dial):
                        local_part = raw_num[len(clean_dial):]
                        display_num = f"{dial_code} {local_part}"
                    else:
                        display_num = f"+{raw_num}"
                        
                    # Add to History Log
                    timestamp = time.strftime("%H:%M:%S")
                    item_id = self.tree_history.insert("", 0, values=(timestamp, display_num, self.selected_operator.upper(), "Waiting for SMS..."))
                    self.history_items[raw_num] = item_id
                        
                    self.root.after(0, lambda d=display_num: self.lbl_number.config(text=d, fg="#10b981"))
                    self.root.after(0, lambda: self.btn_get_number.config(text="Get New Number", state="normal"))
                    self.root.after(0, lambda: self.btn_test_sms.config(state="normal"))
                    self.root.after(0, lambda: self.btn_refresh_sms.config(state="normal"))
                    self.start_polling()
                else:
                    self.root.after(0, lambda: self.lbl_number.config(text="Failed to get number", fg="#ef4444"))
                    self.root.after(0, lambda: self.btn_get_number.config(state="normal"))
            except Exception as e:
                self.root.after(0, lambda: self.lbl_number.config(text="Error fetching number", fg="#ef4444"))
                self.root.after(0, lambda: self.btn_get_number.config(state="normal"))
                
        threading.Thread(target=fetch, daemon=True).start()

    def start_polling(self):
        self.lbl_sms.config(text="Waiting for SMS...", fg="#f59e0b")
        
        def poll():
            for _ in range(15):
                time.sleep(5)
                try:
                    res = requests.get(f"{BASE_URL}/get_messages", params={"token": TOKEN, "number": self.current_number}, timeout=10)
                    raw_response = f"[{res.status_code}] {res.text}"
                    self.root.after(0, lambda r=raw_response: self.update_raw_output(r))
                    
                    if res.status_code == 200:
                        data = res.json()
                        sms_text = str(data)
                        self.root.after(0, lambda d=sms_text: self.lbl_sms.config(text=f"SMS RECEIVED: {d}", fg="#10b981"))
                        
                        # Update History Log
                        def update_history(sms=sms_text, num=self.current_number):
                            if num in self.history_items:
                                item_id = self.history_items[num]
                                vals = self.tree_history.item(item_id, 'values')
                                self.tree_history.item(item_id, values=(vals[0], vals[1], vals[2], sms), tags=("arrived",))
                        self.root.after(0, update_history)
                        return
                except Exception as e:
                    self.root.after(0, lambda err=str(e): self.update_raw_output(f"Exception: {err}"))
            self.root.after(0, lambda: self.lbl_sms.config(text="Timed out waiting for SMS.", fg="#ef4444"))
            
        threading.Thread(target=poll, daemon=True).start()

    def refresh_sms(self):
        if not self.current_number: return
        
        self.btn_refresh_sms.config(state="disabled")
        self.lbl_sms.config(text="Checking for SMS...", fg="#f59e0b")
        
        def refresh():
            try:
                res = requests.get(f"{BASE_URL}/get_messages", params={"token": TOKEN, "number": self.current_number}, timeout=10)
                raw_response = f"[{res.status_code}] {res.text}"
                self.root.after(0, lambda r=raw_response: self.update_raw_output(r))
                
                if res.status_code == 200:
                    data = res.json()
                    sms_text = str(data)
                    self.root.after(0, lambda d=sms_text: self.lbl_sms.config(text=f"SMS RECEIVED: {d}", fg="#10b981"))
                    
                    def update_history(sms=sms_text, num=self.current_number):
                        if num in self.history_items:
                            item_id = self.history_items[num]
                            vals = self.tree_history.item(item_id, 'values')
                            self.tree_history.item(item_id, values=(vals[0], vals[1], vals[2], sms), tags=("arrived",))
                    self.root.after(0, update_history)
                elif res.status_code == 400:
                    try:
                        data = res.json()
                        if data.get("detail") == "No messages found for the provided number":
                            self.root.after(0, lambda: self.lbl_sms.config(text="No messages yet.", fg="#f59e0b"))
                        else:
                            self.root.after(0, lambda d=str(data): self.lbl_sms.config(text=f"API Error: {d}", fg="#ef4444"))
                    except:
                        self.root.after(0, lambda: self.lbl_sms.config(text="No messages yet.", fg="#f59e0b"))
                else:
                    self.root.after(0, lambda c=res.status_code: self.lbl_sms.config(text=f"API Error {c}", fg="#ef4444"))
            except Exception as e:
                self.root.after(0, lambda err=str(e): self.lbl_sms.config(text=f"Error checking SMS: {err}", fg="#ef4444"))
            finally:
                self.root.after(0, lambda: self.btn_refresh_sms.config(state="normal"))
                
        threading.Thread(target=refresh, daemon=True).start()

    def send_test_sms(self):
        if not self.current_number: return
        
        self.btn_test_sms.config(state="disabled")
        self.lbl_sms.config(text="Sending test SMS via Textbelt...", fg="#f59e0b")
        
        def send():
            try:
                # Textbelt expects a leading '+' for international numbers
                target_num = f"+{self.current_number}" if not self.current_number.startswith('+') else self.current_number
                
                payload = {
                    "phone": target_num,
                    "message": "Project Pulse Test SMS: Your number is active and successfully receiving messages!",
                    "key": "textbelt"
                }
                
                res = requests.post("https://textbelt.com/text", data=payload, timeout=10)
                data = res.json()
                
                if data.get("success"):
                    self.root.after(0, lambda: messagebox.showinfo("SMS Sent!", f"Test message successfully dispatched to {target_num}!\n\nWait a few seconds for the auto-poller to pick it up."))
                else:
                    error_msg = data.get('error', 'Unknown Error')
                    self.root.after(0, lambda e=error_msg: messagebox.showwarning("Textbelt Limit Reached", f"Textbelt API Failed:\n\n{e}\n\n(Note: The free tier only allows 1 test SMS per day per IP address)"))
            except Exception as e:
                self.root.after(0, lambda err=e: messagebox.showerror("API Error", f"Failed to contact Textbelt: {err}"))
            finally:
                self.root.after(0, lambda: self.btn_test_sms.config(state="normal"))
                
        threading.Thread(target=send, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SMSAutomationApp(root)
    root.mainloop()

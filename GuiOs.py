import tkinter as tk
from tkinter import ttk, messagebox
import random

class CPUSchedulerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pastel CPU Scheduling Simulator")
        self.root.geometry("1000x750")
        self.root.configure(bg="#E6E6FA")  # Lavender background
        self.processes = []
        self.current_algorithm = "RR"
        self.is_preemptive = tk.BooleanVar(value=False)
        self.show_landing_page()

    def show_landing_page(self):
        self.clear_window()
        
        # Pastel header
        header_canvas = tk.Canvas(self.root, height=100, bg="#E6E6FA", highlightthickness=0)
        header_canvas.pack(fill="x")
        header_canvas.create_rectangle(0, 0, 1000, 100, fill="#FFB6C1", outline="")  # Light pink gradient
        header_canvas.create_text(500, 50, text="CPU Scheduling Simulator", 
                                font=("Helvetica", 28, "bold"), fill="#4B0082")  # Indigo text
        
        algo_frame = ttk.LabelFrame(self.root, text="Choose Your Algorithm", padding=15, 
                                  style="Pastel.TLabelframe")
        algo_frame.pack(pady=30, padx=30, fill="x")
        
        algorithms = [("FCFS", "FCFS"), ("SJF", "SJF"), ("Priority", "PP"), ("Round Robin", "RR")]
        self.algo_var = tk.StringVar(value="RR")
        
        for i, (text, value) in enumerate(algorithms):
            btn = ttk.Radiobutton(algo_frame, text=text, value=value, variable=self.algo_var, 
                                command=self.set_algorithm, style="Pastel.TRadiobutton")
            btn.grid(row=0, column=i, padx=10, pady=10)
        
        ttk.Checkbutton(algo_frame, text="Enable Preemption (SJF/PP)", variable=self.is_preemptive, 
                       style="Pastel.TCheckbutton").grid(row=1, column=1, columnspan=2, pady=10)
        
        ttk.Button(self.root, text="Launch Simulation", command=self.show_execution_page, 
                  style="Launch.TButton").pack(pady=40)

    def set_algorithm(self):
        self.current_algorithm = self.algo_var.get()

    def show_execution_page(self):
        self.clear_window()
        self.create_execution_widgets()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_execution_widgets(self):
        self.root.configure(bg="#E6E6FA")
        
        # Header with pastel gradient
        header_canvas = tk.Canvas(self.root, height=80, bg="#E6E6FA", highlightthickness=0)
        header_canvas.pack(fill="x")
        header_canvas.create_rectangle(0, 0, 1000, 80, fill="#FFB6C1", outline="")  # Light pink
        header_canvas.create_text(500, 40, text=f"{self.current_algorithm} Scheduling {'(Preemptive)' if self.is_preemptive.get() and self.current_algorithm in ['SJF', 'PP'] else '(Non-Preemptive)'}", 
                                font=("Helvetica", 20, "bold"), fill="#4B0082")
        
        back_btn = ttk.Button(header_canvas, text="← Back", command=self.show_landing_page, 
                            style="Back.TButton")
        back_btn.place(x=20, y=20)

        input_frame = ttk.LabelFrame(self.root, text="Add Process", padding=15, 
                                   style="Pastel.TLabelframe")
        input_frame.pack(pady=20, padx=30, fill="x")

        labels = ["Process ID:", "Arrival Time:", "Burst Time:", "Priority:"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(input_frame, text=label, style="Input.TLabel").grid(row=0, column=i*2, padx=5, pady=10)
            entry = ttk.Entry(input_frame, style="Pastel.TEntry")
            entry.grid(row=0, column=i*2+1, padx=5, pady=10)
            self.entries[label] = entry

        if self.current_algorithm == "RR":
            ttk.Label(input_frame, text="Time Quantum:", style="Input.TLabel").grid(row=1, column=0, padx=5, pady=10)
            self.quantum_entry = ttk.Entry(input_frame, style="Pastel.TEntry")
            self.quantum_entry.grid(row=1, column=1, padx=5, pady=10)

        ttk.Button(input_frame, text="Add", command=self.add_process, 
                  style="Action.TButton").grid(row=0, column=8, padx=10, pady=10)
        ttk.Button(input_frame, text="Simulate", command=self.simulate, 
                  style="Action.TButton").grid(row=1, column=8, padx=10, pady=10)

        self.canvas = tk.Canvas(self.root, width=900, height=300, bg="#F0F8FF", highlightthickness=1, 
                              highlightbackground="#4682B4")  # Alice Blue with Steel Blue border
        self.canvas.pack(pady=20, padx=30)

        self.result_text = tk.Text(self.root, height=14, width=100, font=("Courier", 11), 
                                 bg="#F0F8FF", fg="#483D8B", relief="flat", borderwidth=2, 
                                 highlightthickness=1, highlightbackground="#4682B4")
        self.result_text.pack(pady=20, padx=30)

        # Custom styles
        style = ttk.Style()
        style.configure("Pastel.TLabelframe", background="#F0F8FF", foreground="#4682B4")
        style.configure("Pastel.TLabelframe.Label", font=("Helvetica", 12, "bold"), foreground="#FF69B4")  # Hot Pink
        style.configure("Pastel.TRadiobutton", background="#F0F8FF", foreground="#483D8B", 
                       font=("Helvetica", 11, "bold"))
        style.map("Pastel.TRadiobutton", background=[("active", "#D8BFD8")])  # Thistle
        style.configure("Pastel.TCheckbutton", background="#F0F8FF", foreground="#483D8B", 
                       font=("Helvetica", 11))
        style.configure("Launch.TButton", font=("Helvetica", 12, "bold"), background="#87CEEB", 
                       foreground="#191970", padding=10)  # Sky Blue with Midnight Blue text
        style.map("Launch.TButton", background=[("active", "#ADD8E6")])  # Light Blue
        style.configure("Back.TButton", font=("Helvetica", 10, "bold"), background="#DDA0DD", 
                       foreground="#4B0082")  # Plum with Indigo text
        style.map("Back.TButton", background=[("active", "#D8BFD8")])  # Thistle
        style.configure("Input.TLabel", background="#F0F8FF", foreground="#4682B4", 
                       font=("Helvetica", 11, "bold"))
        style.configure("Pastel.TEntry", font=("Helvetica", 11), background="#FFF0F5")  # Lavender Blush
        style.configure("Action.TButton", font=("Helvetica", 11, "bold"), background="#98FB98", 
                       foreground="#006400", padding=6)  # Pale Green with Dark Green text
        style.map("Action.TButton", background=[("active", "#90EE90")])  # Light Green

    def add_process(self):
        try:
            pid = self.entries["Process ID:"].get()
            arrival = int(self.entries["Arrival Time:"].get())
            burst = int(self.entries["Burst Time:"].get())
            priority = int(self.entries["Priority:"].get() or 0)
            if pid and arrival >= 0 and burst > 0:
                self.processes.append({"pid": pid, "arrival": arrival, "burst": burst, 
                                     "remaining": burst, "priority": priority})
                self.result_text.insert(tk.END, f"Added Process {pid}: Arrival={arrival}, Burst={burst}, Priority={priority}\n")
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter valid process details")
        except ValueError:
            messagebox.showerror("Error", "Arrival, Burst, and Priority must be numbers")

    def simulate(self):
        if not self.processes:
            messagebox.showerror("Error", "No processes to simulate")
            return

        self.canvas.delete("all")
        self.result_text.delete(1.0, tk.END)
        
        if self.current_algorithm == "RR":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantum value")
                return
            self.simulate_rr(quantum)
        elif self.current_algorithm == "FCFS":
            self.simulate_fcfs()
        elif self.current_algorithm == "SJF":
            if self.is_preemptive.get():
                self.simulate_sjf_preemptive()
            else:
                self.simulate_sjf_non_preemptive()
        else:  # PP
            if self.is_preemptive.get():
                self.simulate_pp_preemptive()
            else:
                self.simulate_pp_non_preemptive()

    def animate_gantt(self, timeline):
        self.canvas.delete("all")
        x_start = 20
        y = 120
        height = 50
        current_x = x_start
        
        self.canvas.create_line(10, y-30, 880, y-30, arrow=tk.LAST, fill="#4682B4", width=2)
        self.canvas.create_text(20, y-50, text="Time", font=("Helvetica", 12, "bold"), fill="#4682B4")

        def animate_block(index=0):
            if index >= len(timeline):
                self.canvas.create_text(current_x, y-30, text=str(timeline[-1]["start"] + timeline[-1]["duration"]), 
                                      font=("Helvetica", 10), fill="#4682B4")
                return
            
            entry = timeline[index]
            width = entry["duration"] * 25
            base_color = random.choice(["#FFB6C1", "#87CEEB", "#98FB98", "#DDA0DD", "#F0E68C"])  # Pastel palette
            rect_id = self.canvas.create_rectangle(current_x, y, current_x, y + height, fill=base_color, outline="")
            text_id = self.canvas.create_text(current_x + width/2, y + height/2, text=entry["pid"], 
                                            font=("Helvetica", 12, "bold"), fill="#483D8B")
            start_text = self.canvas.create_text(current_x, y-30, text=str(entry["start"]), 
                                               font=("Helvetica", 10), fill="#4682B4")

            def update_frame(frame=0):
                nonlocal current_x
                if frame <= 15:
                    progress = frame / 15
                    new_x = current_x + (width * progress)
                    self.canvas.coords(rect_id, current_x, y, new_x, y + height)
                    self.canvas.coords(text_id, current_x + (width * progress)/2, y + height/2)
                    self.root.after(60, update_frame, frame + 1)
                else:
                    self.canvas.coords(rect_id, current_x, y, current_x + width, y + height)
                    current_x += width + 8
                    animate_block(index + 1)

            update_frame()

        animate_block()

    def simulate_fcfs(self):
        self.result_text.insert(tk.END, "Starting FCFS Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        processes = sorted(self.processes[:], key=lambda x: x["arrival"])
        
        for process in processes:
            if time_elapsed < process["arrival"]:
                time_elapsed = process["arrival"]
            timeline.append({"pid": process["pid"], "start": time_elapsed, "duration": process["burst"]})
            time_elapsed += process["burst"]
            completed.append({
                "pid": process["pid"], "arrival": process["arrival"], "burst": process["burst"],
                "completion": time_elapsed, "priority": process["priority"]
            })
            self.result_text.insert(tk.END, f"Time {time_elapsed-process['burst']}-{time_elapsed}: "
                                  f"Process {process['pid']} executing\n")
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def simulate_sjf_non_preemptive(self):
        self.result_text.insert(tk.END, "Starting SJF Non-Preemptive Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        remaining = sorted(self.processes[:], key=lambda x: x["arrival"])
        
        while remaining:
            available = [p for p in remaining if p["arrival"] <= time_elapsed]
            if not available:
                time_elapsed = min(p["arrival"] for p in remaining)
                continue
            process = min(available, key=lambda x: x["remaining"])
            timeline.append({"pid": process["pid"], "start": time_elapsed, "duration": process["burst"]})
            time_elapsed += process["burst"]
            completed.append({
                "pid": process["pid"], "arrival": process["arrival"], "burst": process["burst"],
                "completion": time_elapsed, "priority": process["priority"]
            })
            self.result_text.insert(tk.END, f"Time {time_elapsed-process['burst']}-{time_elapsed}: "
                                  f"Process {process['pid']} executing\n")
            remaining.remove(process)
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def simulate_sjf_preemptive(self):
        self.result_text.insert(tk.END, "Starting SJF Preemptive Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        remaining = sorted(self.processes[:], key=lambda x: x["arrival"])
        current_process = None
        
        while remaining or current_process:
            available = [p for p in remaining if p["arrival"] <= time_elapsed]
            if not available and not current_process:
                time_elapsed = min(p["arrival"] for p in remaining)
                continue
            
            if available:
                next_process = min(available, key=lambda x: x["remaining"])
                if current_process and current_process["remaining"] > next_process["remaining"]:
                    remaining.append(current_process)
                    current_process = next_process
                    remaining.remove(next_process)
                elif not current_process:
                    current_process = next_process
                    remaining.remove(next_process)
            
            if current_process:
                exec_time = 1
                timeline.append({"pid": current_process["pid"], "start": time_elapsed, "duration": exec_time})
                current_process["remaining"] -= exec_time
                time_elapsed += exec_time
                self.result_text.insert(tk.END, f"Time {time_elapsed-exec_time}-{time_elapsed}: "
                                      f"Process {current_process['pid']} executing\n")
                
                if current_process["remaining"] == 0:
                    completed.append({
                        "pid": current_process["pid"], "arrival": current_process["arrival"],
                        "burst": current_process["burst"], "completion": time_elapsed,
                        "priority": current_process["priority"]
                    })
                    current_process = None
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def simulate_pp_non_preemptive(self):
        self.result_text.insert(tk.END, "Starting Priority Non-Preemptive Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        remaining = sorted(self.processes[:], key=lambda x: x["arrival"])
        
        while remaining:
            available = [p for p in remaining if p["arrival"] <= time_elapsed]
            if not available:
                time_elapsed = min(p["arrival"] for p in remaining)
                continue
            process = min(available, key=lambda x: x["priority"])
            timeline.append({"pid": process["pid"], "start": time_elapsed, "duration": process["burst"]})
            time_elapsed += process["burst"]
            completed.append({
                "pid": process["pid"], "arrival": process["arrival"], "burst": process["burst"],
                "completion": time_elapsed, "priority": process["priority"]
            })
            self.result_text.insert(tk.END, f"Time {time_elapsed-process['burst']}-{time_elapsed}: "
                                  f"Process {process['pid']} executing\n")
            remaining.remove(process)
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def simulate_pp_preemptive(self):
        self.result_text.insert(tk.END, "Starting Priority Preemptive Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        remaining = sorted(self.processes[:], key=lambda x: x["arrival"])
        current_process = None
        
        while remaining or current_process:
            available = [p for p in remaining if p["arrival"] <= time_elapsed]
            if not available and not current_process:
                time_elapsed = min(p["arrival"] for p in remaining)
                continue
            
            if available:
                next_process = min(available, key=lambda x: x["priority"])
                if current_process and current_process["priority"] > next_process["priority"]:
                    remaining.append(current_process)
                    current_process = next_process
                    remaining.remove(next_process)
                elif not current_process:
                    current_process = next_process
                    remaining.remove(next_process)
            
            if current_process:
                exec_time = 1
                timeline.append({"pid": current_process["pid"], "start": time_elapsed, "duration": exec_time})
                current_process["remaining"] -= exec_time
                time_elapsed += exec_time
                self.result_text.insert(tk.END, f"Time {time_elapsed-exec_time}-{time_elapsed}: "
                                      f"Process {current_process['pid']} executing\n")
                
                if current_process["remaining"] == 0:
                    completed.append({
                        "pid": current_process["pid"], "arrival": current_process["arrival"],
                        "burst": current_process["burst"], "completion": time_elapsed,
                        "priority": current_process["priority"]
                    })
                    current_process = None
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def simulate_rr(self, quantum):
        self.result_text.insert(tk.END, "Starting Round Robin Simulation...\n\n")
        time_elapsed = 0
        completed = []
        timeline = []
        remaining = sorted(self.processes[:], key=lambda x: x["arrival"])
        queue = []
        
        while remaining or queue:
            while remaining and remaining[0]["arrival"] <= time_elapsed:
                queue.append(remaining.pop(0))
            if not queue:
                time_elapsed = remaining[0]["arrival"]
                continue
                
            process = queue.pop(0)
            exec_time = min(quantum, process["remaining"])
            timeline.append({"pid": process["pid"], "start": time_elapsed, "duration": exec_time})
            process["remaining"] -= exec_time
            time_elapsed += exec_time
            
            self.result_text.insert(tk.END, f"Time {time_elapsed-exec_time}-{time_elapsed}: "
                                  f"Process {process['pid']} executing\n")
            
            if process["remaining"] > 0:
                queue.append(process)
            else:
                completed.append({
                    "pid": process["pid"], "arrival": process["arrival"], "burst": process["burst"],
                    "completion": time_elapsed, "priority": process["priority"]
                })
        
        self.display_results(completed)
        self.animate_gantt(timeline)

    def display_results(self, completed):
        self.result_text.insert(tk.END, "\nSimulation Completed!\n")
        self.result_text.insert(tk.END, "Process Statistics:\n")
        
        avg_waiting = 0
        for proc in completed:
            waiting = proc["completion"] - proc["arrival"] - proc["burst"]
            avg_waiting += waiting
            self.result_text.insert(tk.END, f"Process {proc['pid']}: Waiting Time = {waiting}, "
                                  f"Turnaround Time = {proc['completion'] - proc['arrival']}\n")
        
        avg_waiting /= len(completed)
        self.result_text.insert(tk.END, f"\nAverage Waiting Time: {avg_waiting:.2f}")
        self.processes.clear()

def main():
    root = tk.Tk()
    app = CPUSchedulerSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

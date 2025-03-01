import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoanHistogram:
    def __init__(self, data_file="data.txt", theme="light", days=30):
        self.data_file = data_file
        self.days = days
        self.set_theme(theme)
        self.loan_data = {}
        self.load_data()

    def load_data(self):
        self.loan_data = {}
        try:
            with open(self.data_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        date_str, value_str = line.split(":")
                        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
                        value = float(value_str)
                        self.loan_data[date_obj] = value
                    except Exception as e:
                        print(f"Skipping invalid line: {line} ({e})")
        except FileNotFoundError:
            print(f"Data file '{self.data_file}' not found!")

    def set_theme(self, theme):
        self.theme = theme.lower()
        if self.theme == "dark":
            self.bg_color = "#1e1e1e"
        else:
            self.bg_color = "#fff"

    def get_previous_days_data(self):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=self.days - 1)
        dates = [start_date + datetime.timedelta(days=i) for i in range(self.days)]
        values = [self.loan_data.get(day, 0) for day in dates]
        return dates, values

    def create_figure(self):
        dates, values = self.get_previous_days_data()
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        bar_container = ax.bar(dates, values, color="red", edgecolor="none")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        fig.autofmt_xdate()
        for spine in ax.spines.values():
            spine.set_visible(False)
        tick_color = "black" if self.bg_color == "#fff" else "white"
        ax.tick_params(colors=tick_color)
        ax.title.set_color(tick_color)
        ax.xaxis.label.set_color(tick_color)
        ax.yaxis.label.set_color(tick_color)
        ax.grid(False)
        max_value = max(values)
        ax.set_ylim(top=max_value + 10)
        annot = ax.annotate(
            "", 
            xy=(0, 0), 
            xytext=(10, 10), 
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w" if self.bg_color == "#fff" else "gray", ec="none", alpha=0.8),
            arrowprops=dict(arrowstyle="->")
        )
        annot.set_visible(False)

        def update_annot(bar, date_value):
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_height()
            annot.xy = (x, y)
            text = f"{date_value.strftime('%d-%m-%Y')}\nEmprunts: {int(y)}"
            annot.set_text(text)
            annot.get_bbox_patch().set_facecolor("w" if self.bg_color == "#fff" else "gray")
            annot.get_bbox_patch().set_edgecolor("none")
            annot.get_bbox_patch().set_alpha(0.8)

        def on_hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                for bar, date_value in zip(bar_container.patches, dates):
                    contains, _ = bar.contains(event)
                    if contains:
                        update_annot(bar, date_value)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_hover)
        plt.margins(x=0)
        plt.tight_layout(pad=1)
        return fig

    def embed_in_tkinter(self, master):
        fig = self.create_figure()
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        return canvas

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Loan Histogram with Date Range Filter")
    histogram = LoanHistogram(data_file="data.txt", theme="light", days=30)

    def change_theme(event):
        selected_theme = theme_selector.get()
        histogram.set_theme(selected_theme)
        update_chart()

    def change_range(event):
        try:
            selected_days = int(range_selector.get())
            histogram.days = selected_days
            update_chart()
        except ValueError:
            pass

    def update_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()
        histogram.embed_in_tkinter(chart_frame)

    control_frame = ttk.Frame(root)
    control_frame.pack(fill=tk.X, padx=0, pady=5)
    ttk.Label(control_frame, text="Select Theme:").pack(side=tk.LEFT, padx=(0, 5))
    theme_selector = ttk.Combobox(control_frame, values=["light", "dark"], state="readonly", width=8)
    theme_selector.current(0)
    theme_selector.pack(side=tk.LEFT, padx=(0, 10))
    theme_selector.bind("<<ComboboxSelected>>", change_theme)
    ttk.Label(control_frame, text="Select Range (days):").pack(side=tk.LEFT, padx=(0, 5))
    range_selector = ttk.Combobox(control_frame, values=["7", "14", "30"], state="readonly", width=5)
    range_selector.current(2)
    range_selector.pack(side=tk.LEFT)
    range_selector.bind("<<ComboboxSelected>>", change_range)
    chart_frame = ttk.Frame(root)
    chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    histogram.embed_in_tkinter(chart_frame)
    root.mainloop()

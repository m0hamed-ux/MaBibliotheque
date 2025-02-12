import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator
import mplcursors
from datetime import datetime, timedelta
import pandas as pd
from scipy.interpolate import CubicSpline
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class LoanChart:
    def __init__(self, dayrange, theme, filename):
        self.filename = filename
        self.current_theme = theme
        if theme == 'dark':
            self.theme = {
                'background': '#1e1e1e',
                'text': '#ffffff',
                'accent': '#3fdfff',
                'grid': '#333333',
                'gradient_colors': ['#00ff9f', '#00b8ff'],
                'annotation_bg': '#2d2d2d',
                'moving_average': '#888888',
                'min_marker': '#ff6b6b',
                'max_marker': '#4ecdc4',
                'theme': 'dark'
            }
        else:
            self.theme = {
                'background': '#ffffff',
                'text': '#000000',
                'accent': '#3fdfff',
                'grid': '#e0e0e0',
                'gradient_colors': ['#00ff9f', '#00b8ff'],
                'annotation_bg': '#f0f0f0',
                'moving_average': '#888888',
                'min_marker': '#ff6b6b',
                'max_marker': '#4ecdc4',
                'theme': 'light'
            }
        
        self.config = {
            'figure_size': (12, 7),
            'dpi': 100,
            'show_gradient': True,
            'show_markers': False,
            'marker_size': 2,
            'line_width': 2.5,
            'grid_alpha': 1,
            'smoothing_factor': 100,
            'gradient_opacity': 0.5,
            'show_min_max': True,
            'show_trend_arrow': True
        }
        self.dayrange = dayrange
        
        self._load_data()
        
    def _load_data(self):
        data_points = []
        try:
            with open(self.filename, 'r') as file:
                file_data = {}
                for line in file:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    try:
                        date_str, value_str = line.split(':')
                        date = datetime.strptime(date_str.strip(), '%d-%m-%Y')
                        value = int(value_str.strip())
                        file_data[date] = value
                    except (ValueError, IndexError) as e:
                        print(f"Skipping invalid line: {line}")
                        continue

                today = datetime.now()
                days = self.dayrange if self.dayrange in [30, 14, 7] else 7
                for i in range(days-1, -1, -1):
                    date = today - timedelta(days=i)
                    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
                    if date not in file_data:
                        file_data[date] = 0
                
                data_points = [(date, value) for date, value in sorted(file_data.items())]
                data_points = data_points[-days:]

        except FileNotFoundError:
            print(f"Data file {self.filename} not found. Using sample data.")
            today = datetime.now()
            days = self.dayrange if self.dayrange in [30, 14, 7] else 7
            data_points = [
                (today - timedelta(days=i), 0)
                for i in range(days-1, -1, -1)
            ]
        
        if not data_points:
            print("No valid data found. Using sample data.")
            today = datetime.now()
            data_points = [
                (today - timedelta(days=i), np.random.randint(150, 250))
                for i in range(6, -1, -1)
            ]
        
        self.data = pd.DataFrame(data_points, columns=['date', 'value'])
        self.data = self.data.sort_values('date').reset_index(drop=True)
        
        if len(self.data) > self.dayrange:
            self.data = self.data.tail(self.dayrange).reset_index(drop=True)
        
        if len(self.data) >= 2:
            self.current_value = self.data['value'].iloc[-1]    
            self.previous_value = self.data['value'].iloc[-2]
            self.daily_change = ((self.current_value - self.previous_value) / self.previous_value * 100) if self.previous_value != 0 else 0
            
            start_value = self.data['value'].iloc[0]
            self.weekly_change = ((self.current_value - start_value) / start_value * 100) if start_value != 0 else 0
        else:
            self.current_value = self.data['value'].iloc[-1] if len(self.data) > 0 else 0
            self.previous_value = 0
            self.daily_change = 0
            self.weekly_change = 0
        
        self.data['MA7'] = self.data['value'].rolling(window=min(7, len(self.data)), min_periods=1).mean()
    
    def number_formatter(self, x, p):
        return f'{int(x):,}'
    
    def _style_chart(self, ax):
        ax.yaxis.set_major_formatter(FuncFormatter(self.number_formatter))
        
        trend = '↑' if self.daily_change >= 0 else '↓'
        trend_color = self.theme['accent'] if self.daily_change >= 0 else self.theme['min_marker']
        
        title_text = (
            f'{self.current_value:,} Emprunts\n'
            f'{trend} {abs(self.daily_change):.1f}% Aujourd\'hui'
        )
        
        ax.set_title(title_text,
                    color=trend_color,
                    fontsize=16,
                    pad=20,
                    fontweight='bold')
        
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        ax.grid(True, linestyle='--', alpha=self.config['grid_alpha'], color=self.theme['grid'], linewidth=1)
        ax.set_axisbelow(True)
        
        for spine in ax.spines.values():
            spine.set_color(self.theme['grid'])
            spine.set_linewidth(0.5)
        
        ax.tick_params(colors=self.theme['text'], grid_alpha=self.config['grid_alpha'], length=5)
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')
        
        plt.tight_layout(rect=[0.02, 0, 0.98, 1])
    
    def update_annotation(self, idx, value):
        date = self.data['date'].iloc[idx]
        
        if idx > 0:
            prev_value = self.data['value'].iloc[idx - 1]
            day_change = ((value - prev_value) / prev_value) * 100
            day_text = f'\n{day_change:+.1f}% vs hier'
        else:
            day_text = ''
        
        start_value = self.data['value'].iloc[0]
        wtd_change = ((value - start_value) / start_value) * 100
        if idx > 0:
            wtd_text = f'\n{wtd_change:+.1f}% WTD'
        else:
            wtd_text = ''
        
        weekdays = {
            'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
            'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi',
            'Sunday': 'Dimanche'
        }
        months = {
            'Jan': 'Jan', 'Feb': 'Fév', 'Mar': 'Mar', 'Apr': 'Avr',
            'May': 'Mai', 'Jun': 'Juin', 'Jul': 'Juil', 'Aug': 'Août',
            'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Déc'
        }
        
        weekday = weekdays[date.strftime('%A')]
        month = months[date.strftime('%b')]
        day = date.strftime('%d')
        
        text = (
            f'{weekday}, {day} {month}\n'
            f'{value:,} Emprunts'
            f'{day_text}'
            f'{wtd_text}'
        )
        
        if idx > 0:
            color = self.theme['accent'] if value >= prev_value else self.theme['min_marker']
        else:
            color = self.theme['accent']
        
        return text, color

    def create_chart(self, show_moving_average=False, show_annotations=True):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=self.config['figure_size'], dpi=self.config['dpi'])
        
        fig.patch.set_facecolor(self.theme['background'])
        ax.set_facecolor(self.theme['background'])
        
        x_numeric = np.arange(len(self.data))
        values = self.data['value'].values
        
        x_smooth = np.linspace(0, len(self.data) - 1, self.config['smoothing_factor'])
        
        y_smooth = np.interp(x_smooth, x_numeric, values)
        
        line = ax.plot(x_smooth, y_smooth,
                      color=self.theme['accent'],
                      linewidth=self.config['line_width'],
                      zorder=3)
        
        if self.config['show_markers']:
            ax.scatter(x_numeric, values,
                      color=self.theme['accent'],
                      s=(self.config['marker_size'] * 1.5)**2,
                      zorder=4,
                      alpha=1.0)
        
        gradient_fill = ax.fill_between(
            x_smooth, y_smooth, 
            np.min(values) * 0.95,
            color=self.theme['accent'],
            alpha=0.1,
            zorder=2)
        
        gradient = np.linspace(0, 0.2, 100)
        gradient_rgb = plt.matplotlib.colors.to_rgba_array(self.theme['accent'])
        gradient_rgb = np.tile(gradient_rgb, (100, 1))
        gradient_rgb[:, -1] = gradient
        gradient_fill.set_facecolors(gradient_rgb)
        
        if show_moving_average:
            ax.plot(x_numeric, self.data['MA7'],
                   color=self.theme['moving_average'],
                   linestyle='--',
                   linewidth=1.5,
                   label='7-Day MA',
                   alpha=0.7,
                   zorder=2)
            
            ax.legend(facecolor=self.theme['annotation_bg'],
                     edgecolor=self.theme['grid'],
                     fontsize=10,
                     loc='upper left')
        
        ax.set_xticks(x_numeric)
        ax.set_xticklabels(self.data['date'].dt.strftime('%b %d'), rotation=45)
        
        self._style_chart(ax)
        
        if show_annotations:
            self._add_hover_effect(line[0], ax)
        
        y_min = self.data['value'].min() * 0.95
        y_max = self.data['value'].max() * 1.05
        ax.set_ylim(y_min, y_max)
        ax.set_xlim(0, len(self.data) - 1)
        
        plt.tight_layout(pad=1.5, rect=[0.02, 0, 0.98, 1])
        
        return fig, ax

    def _add_hover_effect(self, line, ax):
        x_numeric = np.arange(len(self.data))
        values = self.data['value'].values
        
        scatter = ax.scatter(x_numeric, values,
                            color=self.theme['accent'],
                            s=100,  
                            alpha=0.0,  
                            picker=True,
                            zorder=5)
        
        tooltip = ax.text(0, 0, '',
                         bbox=dict(
                             boxstyle='round,pad=0.5',
                             fc=self.theme['background'],
                             ec=self.theme['accent'],
                             alpha=0.95
                         ),
                         color=self.theme['text'],
                         fontsize=10,
                         fontweight='bold',
                         ha='center',
                         va='bottom',
                         visible=False,
                         zorder=6)
        
        def hover(event):
            if event.inaxes == ax:
                cont, ind = scatter.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    value = values[idx]
                    
                    text, color = self.update_annotation(idx, value)
                    
                    tooltip.set_text(text)
                    tooltip.set_position((idx, value + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.05))
                    tooltip.set_bbox(dict(
                        boxstyle='round,pad=0.5',
                        fc=self.theme['background'],
                        ec=color,
                        alpha=0.95
                    ))
                    tooltip.set_color(self.theme['text'])
                    tooltip.set_visible(True)
                    
                    scatter.set_sizes([100 if i != idx else 150 for i in range(len(self.data))])
                    scatter.set_alpha(0.7)
                    scatter.set_facecolor(color)
                    
                    plt.draw()
                else:
                    tooltip.set_visible(False)
                    scatter.set_sizes([100] * len(self.data))
                    scatter.set_alpha(0.0)
                    plt.draw()
        
        plt.connect('motion_notify_event', hover)
    def returnTitle(self):
        return f'{self.current_value:,} Emprunts\n↑ {abs(self.daily_change):.1f}% Aujourd\'hui\n↑ {abs(self.weekly_change):.1f}% Cette Semaine'
    def embed_in_tkinter(self, frame):
        fig, ax = self.create_chart()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    def get_theme(self):
        return self.current_theme
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == 'dark':
            self.theme = {
                'background': '#1e1e1e',
                'text': '#ffffff',
                'accent': '#00ff9f',
                'grid': '#333333',
                'gradient_colors': ['#00ff9f', '#00b8ff'],
                'annotation_bg': '#2d2d2d',
                'moving_average': '#888888',
                'min_marker': '#ff6b6b',
                'max_marker': '#4ecdc4',
                'theme': 'dark'
            }
        else:
            self.theme = {
                'background': '#ffffff',
                'text': '#000000',
                'accent': '#00ff9f',
                'grid': '#e0e0e0',
                'gradient_colors': ['#00ff9f', '#00b8ff'],
                'annotation_bg': '#f0f0f0',
                'moving_average': '#888888',
                'min_marker': '#ff6b6b',
                'max_marker': '#4ecdc4',
                'theme': 'light'
            }
    def get_dayrange(self):
        return self.dayrange

def changeTheme(frame, theme, dayrange, filename):
    for widget in frame.winfo_children():
        widget.destroy()
    chart = LoanChart(dayrange, theme, filename)
    chart.embed_in_tkinter(frame)
    return chart
def changeDayrange(frame, dayrange, theme, filename):
    for widget in frame.winfo_children():
        widget.destroy()
    chart = LoanChart(int(dayrange), theme, filename)
    chart.embed_in_tkinter(frame)
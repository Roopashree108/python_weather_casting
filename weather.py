import tkinter as tk
from tkinter import messagebox
import requests

# --- THE LOGIC (Fetching Data & Time Analysis) ---
def get_weather():
    api_key = "7b243593cde809b4a8169148aa8042e2"
    city = city_entry.get()
    
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    # Use the 'forecast' endpoint to get time-stamped data
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # 1. Current Stats (from the first data block)
            current = data['list'][0]
            temp = float(current['main']['temp'])
            humidity = current['main']['humidity']
            desc = current['weather'][0]['description'].capitalize()
            
            # 2. Temperature Color Logic
            if temp > 30.0:
                temp_color = "#E74C3C" # Red
            elif temp > 20.0:
                temp_color = "#F1C40F" # Yellow
            else:
                temp_color = "#3498DB" # Blue
            
            # 3. Time Analysis: Finding next Rain/Sun
            rain_time = "No rain predicted"
            sunny_time = "No clear skies soon"
            
            # Check the next 8 blocks (24 hours)
            for entry in data['list'][:8]:
                condition = entry['weather'][0]['main'].lower()
                time_txt = entry['dt_txt'].split(" ")[1][:5] # Get HH:MM
                
                if "rain" in condition and rain_time == "No rain predicted":
                    rain_time = f"Rain expected at {time_txt}"
                if "clear" in condition and sunny_time == "No clear skies soon":
                    sunny_time = f"Sun expected at {time_txt}"

            # 4. Update the User Interface
            result_label.config(text=f"{temp}°C", fg=temp_color)
            details_label.config(
                text=f"Condition: {desc}\nHumidity: {humidity}%\n\n"
                     f"🌧 {rain_time}\n"
                     f"☀️ {sunny_time}"
            )
            
        else:
            messagebox.showerror("Error", "City not found.")
    except Exception as e:
        messagebox.showerror("Connection Error", "Check your internet connection!")

# --- THE GUI (Visual Window) ---
root = tk.Tk()
root.title("Data Science Weather Dashboard")
root.geometry("400x550")
root.configure(bg="#316FAD")

# Header
tk.Label(root, text="WEATHER TRACKER", font=("Helvetica", 18, "bold"), bg="#3928D8", fg="white").pack(pady=25)

# City Input Box
city_entry = tk.Entry(root, font=("Helvetica", 18), justify='center', highlightthickness=2)
city_entry.insert(0, "Bengaluru")
city_entry.pack(pady=10)

# Fetch Button
search_btn = tk.Button(root, text="GET LIVE DATA", command=get_weather, font=("Helvetica", 12, "bold"), bg="#27AE60", fg="white", padx=20, pady=10)
search_btn.pack(pady=20)

# Large Temperature Display
result_label = tk.Label(root, text="--°C", font=("Helvetica", 50, "bold"), bg="#2C3E50", fg="#BDC3C7")
result_label.pack()

# Detail Text Display
details_label = tk.Label(root, text="Enter a city to start", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1", justify="center", wraplength=350)
details_label.pack(pady=20)

root.mainloop()
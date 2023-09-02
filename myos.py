import time
import psutil
from colorama import Fore, Style

# Define color codes for memory usage levels
COLOR_LOW = Fore.GREEN
COLOR_MODERATE = Fore.YELLOW
COLOR_HIGH = Fore.RED
COLOR_RESET = Style.RESET_ALL

def format_size(size):
    # Format bytes to human-readable size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def get_memory_usage(application_name):
    total_memory = 0
    for process in psutil.process_iter(attrs=['name', 'memory_info']):
        if application_name.lower() in process.info['name'].lower():
            total_memory += process.info['memory_info'].rss
    return total_memory

def display_memory_usage(application_name, sort_by_memory):
    mem_usage = get_memory_usage(application_name)
    mem_percent = (mem_usage / psutil.virtual_memory().total) * 100
    mem_usage_formatted = format_size(mem_usage)

    color_code = COLOR_LOW
    if mem_percent > 30:
        color_code = COLOR_MODERATE
    if mem_percent > 70:
        color_code = COLOR_HIGH

    mem_percent_str = f"{color_code}{mem_percent:.2f}%{COLOR_RESET}"

    output = f"{application_name}\t\t\t{mem_usage_formatted}\t\t\t{mem_percent_str}"
    return output

def main():
    refresh_interval = 2  # Set the refresh interval in seconds
    application_names = ["Code.exe","WhatsApp.exe","Python3.11.exe","explorer.exe"]  # Replace with the applications you want to monitor
    sort_by_memory = False

    print("Application Name\t\t\Memory Usage\tMemory Percentage")
    try:
        while True:
            for app_name in application_names:
                output = display_memory_usage(app_name, sort_by_memory)
                print(output)
            time.sleep(refresh_interval)

    except KeyboardInterrupt:
        print("\nMonitoring terminated.")

if __name__ == "__main__":
    main()

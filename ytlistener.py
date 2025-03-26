import pygetwindow as gw
import time
import subprocess
import re
import atexit

def get_youtube_window_title():
    all_windows = gw.getWindowsWithTitle('')  
    youtube_window = None

    for window in all_windows:
        window_title = window.title
        if 'YouTube' in window_title:
            youtube_window = window_title
            break 

    return youtube_window

def clean_title(title):
    title = re.sub(r'\(\d+\)\s*', '', title)
    title = re.sub(r' - YouTube.*', '', title)
    return title.strip()

def update_readme(title):
    cleaned_title = clean_title(title)
    if len(cleaned_title) > 100:
        cleaned_title = cleaned_title[:100]

    with open('README.md', 'r+', encoding='utf-8') as f:
        content = f.read()
        current_playing_section = "## Vibes in Progress..."

        if current_playing_section in content:
            start_index = content.find(current_playing_section) + len(current_playing_section)
            title_line_start = content.find('Title: ', start_index)
            title_line_end = content.find('\n', title_line_start)
            content = content[:title_line_start] + f"Title: {cleaned_title}\n" + content[title_line_end:]
        else:
            content += f"\n\n## Vibes in Progress...\n\nTitle: {cleaned_title}\n"

        f.seek(0)
        f.write(content)
        f.truncate()

    subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', 'Current Music Update'])
    subprocess.run(['git', 'push'])

def set_no_active_track():
    update_readme("#7: No Track Found, SL3EP1N6 T1M3 ᶻ 𝗓 𐰁✰")

def refresh_window_title():
    last_title = None
    atexit.register(set_no_active_track)

    while True:
        title = get_youtube_window_title()

        if title:
            if title != last_title:
                print(f"Active title: {title}")
                update_readme(title)
                last_title = title
        elif last_title is not None:
            update_readme("#7: No Track Found, SL3EP1N6 T1M3 ᶻ 𝗓 𐰁✰")
            last_title = None

        time.sleep(5)

if __name__ == "__main__":
    refresh_window_title()

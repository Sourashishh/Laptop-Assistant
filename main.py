import speech_recognition as sr
import pyttsx3
import subprocess
import platform
import os
import webbrowser
import time
from datetime import datetime
import pyautogui
import winreg  # For Windows registry access
from pathlib import Path

class UniversalVoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 0.9)
        
        # Get OS type
        self.os_type = platform.system()
        
        # Cache for discovered applications
        self.app_cache = {}
        
        print("🔍 Scanning your system for installed applications...")
        self.scan_system_apps()
        print(f"✅ Found {len(self.app_cache)} applications!")
        
    def scan_system_apps(self):
        """Scan system for all installed applications"""
        if self.os_type == "Windows":
            self._scan_windows_apps()
        elif self.os_type == "Darwin":
            self._scan_macos_apps()
        else:
            self._scan_linux_apps()
    
    def _scan_windows_apps(self):
        """Scan Windows for installed applications"""
        # Common installation directories
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
            os.path.expandvars(r"%APPDATA%"),
        ]
        
        # Scan directories for .exe files
        for base_path in search_paths:
            if os.path.exists(base_path):
                try:
                    for root, dirs, files in os.walk(base_path):
                        # Limit depth to avoid too deep scanning
                        depth = root[len(base_path):].count(os.sep)
                        if depth > 3:
                            continue
                        
                        for file in files:
                            if file.endswith('.exe'):
                                app_name = file.replace('.exe', '').lower()
                                app_path = os.path.join(root, file)
                                
                                # Store multiple variations of the name
                                self.app_cache[app_name] = app_path
                                
                                # Also store by folder name
                                folder_name = os.path.basename(root).lower()
                                if folder_name and folder_name not in self.app_cache:
                                    self.app_cache[folder_name] = app_path
                except (PermissionError, OSError):
                    continue
        
        # Add Windows built-in apps
        builtin_apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'wordpad': 'write.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe',
            'settings': 'ms-settings:',
        }
        self.app_cache.update(builtin_apps)
        
        # Try to get apps from Start Menu registry
        try:
            self._scan_windows_registry()
        except:
            pass
    
    def _scan_windows_registry(self):
        """Scan Windows Registry for installed programs"""
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for reg_path in registry_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        try:
                            app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            app_path = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                            
                            if app_name and app_path:
                                # Clean the path (remove quotes and arguments)
                                app_path = app_path.split(',')[0].strip('"')
                                if os.path.exists(app_path):
                                    self.app_cache[app_name.lower()] = app_path
                        except:
                            pass
                        
                        winreg.CloseKey(subkey)
                    except:
                        continue
                
                winreg.CloseKey(key)
            except:
                continue
    
    def _scan_macos_apps(self):
        """Scan macOS for installed applications"""
        search_paths = [
            "/Applications",
            os.path.expanduser("~/Applications"),
            "/System/Applications",
            "/System/Applications/Utilities"
        ]
        
        for base_path in search_paths:
            if os.path.exists(base_path):
                try:
                    for item in os.listdir(base_path):
                        if item.endswith('.app'):
                            app_name = item.replace('.app', '').lower()
                            app_path = os.path.join(base_path, item)
                            self.app_cache[app_name] = app_path
                except (PermissionError, OSError):
                    continue
    
    def _scan_linux_apps(self):
        """Scan Linux for installed applications"""
        # Check common binary paths
        search_paths = ['/usr/bin', '/usr/local/bin', '/snap/bin']
        
        for path in search_paths:
            if os.path.exists(path):
                try:
                    for file in os.listdir(path):
                        file_path = os.path.join(path, file)
                        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                            self.app_cache[file.lower()] = file
                except (PermissionError, OSError):
                    continue
        
        # Parse .desktop files
        desktop_paths = [
            '/usr/share/applications',
            os.path.expanduser('~/.local/share/applications')
        ]
        
        for desktop_path in desktop_paths:
            if os.path.exists(desktop_path):
                try:
                    for file in os.listdir(desktop_path):
                        if file.endswith('.desktop'):
                            app_name = file.replace('.desktop', '').lower()
                            self.app_cache[app_name] = file.replace('.desktop', '')
                except (PermissionError, OSError):
                    continue
    
    def find_app(self, app_name):
        """Find application path by name (fuzzy matching)"""
        app_name = app_name.lower().strip()
        
        # Direct match
        if app_name in self.app_cache:
            return self.app_cache[app_name]
        
        # Partial match
        for key, path in self.app_cache.items():
            if app_name in key or key in app_name:
                return path
        
        # Word match
        app_words = app_name.split()
        for key, path in self.app_cache.items():
            key_words = key.split()
            if any(word in key_words for word in app_words):
                return path
        
        return None
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice command"""
        with self.microphone as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"👤 You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return ""
            except sr.RequestError:
                self.speak("Sorry, speech service is unavailable.")
                return ""
    
    def open_application(self, app_name):
        """Open any application"""
        app_path = self.find_app(app_name)
        
        if app_path:
            try:
                if self.os_type == "Windows":
                    # Try different methods
                    if app_path.startswith('ms-'):
                        # Windows URI scheme
                        os.startfile(app_path)
                    elif os.path.exists(app_path):
                        os.startfile(app_path)
                    else:
                        subprocess.Popen(app_path, shell=True)
                    
                    self.speak(f"Opening {app_name}")
                    return True
                    
                elif self.os_type == "Darwin":
                    subprocess.Popen(['open', '-a', app_path])
                    self.speak(f"Opening {app_name}")
                    return True
                    
                else:  # Linux
                    subprocess.Popen(app_path, shell=True)
                    self.speak(f"Opening {app_name}")
                    return True
                    
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                self.speak(f"Sorry, I had trouble opening {app_name}")
                return False
        else:
            self.speak(f"Sorry, I couldn't find {app_name} on your system")
            return False
    
    def open_website(self, site_name):
        """Open popular websites"""
        websites = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'gmail': 'https://mail.google.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://www.reddit.com',
            'amazon': 'https://www.amazon.com',
            'netflix': 'https://www.netflix.com',
            'whatsapp': 'https://web.whatsapp.com',
        }
        
        url = websites.get(site_name, f'https://www.{site_name}.com')
        webbrowser.open(url)
        self.speak(f"Opening {site_name}")
    
    def youtube_search(self, query):
        """Search and play on YouTube - opens first video directly"""
        search_query = query.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        
        # Wait for page to load then click first video
        time.sleep(4)
        try:
            # Press Tab to focus on first video, then Enter to play it
            pyautogui.press('tab', presses=3, interval=0.3)
            pyautogui.press('enter')
            self.speak(f"Playing {query} on YouTube")
        except:
            self.speak(f"Opened search results for {query}")
    
    def play_song_youtube(self, song_name):
        """Play a specific song on YouTube - opens the first video directly"""
        search_query = song_name.replace(' ', '+')
        # Use YouTube search that auto-plays first result
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        
        # Wait for page to load then click first video
        time.sleep(4)
        try:
            # Press Tab to focus on first video, then Enter to play it
            pyautogui.press('tab', presses=3, interval=0.3)
            pyautogui.press('enter')
            self.speak(f"Playing {song_name} on YouTube")
        except:
            self.speak(f"Opened search results for {song_name}. Please click the video you want.")
    
    def google_search(self, query):
        """Search on Google"""
        search_query = query.replace(' ', '+')
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        self.speak(f"Searching for {query} on Google")
    
    def get_time(self):
        """Tell current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current_time}")
    
    def get_date(self):
        """Tell current date"""
        current_date = datetime.now().strftime("%B %d, %Y")
        day = datetime.now().strftime("%A")
        self.speak(f"Today is {day}, {current_date}")
    
    def close_application(self, app_name):
        """Close an application"""
        try:
            if self.os_type == "Windows":
                # Try to find the process name
                app_path = self.find_app(app_name)
                if app_path:
                    process_name = os.path.basename(app_path)
                    subprocess.run(f"taskkill /f /im {process_name}", shell=True)
                    self.speak(f"Closing {app_name}")
                else:
                    self.speak(f"Could not find {app_name} to close")
            elif self.os_type == "Darwin":
                subprocess.run(f"pkill -x '{app_name}'", shell=True)
                self.speak(f"Closing {app_name}")
            else:
                subprocess.run(f"pkill {app_name}", shell=True)
                self.speak(f"Closing {app_name}")
        except Exception as e:
            self.speak(f"Could not close {app_name}")
            print(f"Error: {e}")
    
    def volume_control(self, action):
        """Control system volume"""
        try:
            if action == "up" or action == "increase":
                pyautogui.press("volumeup", presses=5)
                self.speak("Volume increased")
            elif action == "down" or action == "decrease":
                pyautogui.press("volumedown", presses=5)
                self.speak("Volume decreased")
            elif action == "mute":
                pyautogui.press("volumemute")
                self.speak("Volume muted")
        except:
            self.speak("Could not control volume")
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            self.speak(f"Screenshot saved as {filename}")
        except:
            self.speak("Could not take screenshot")
    
    def list_apps(self):
        """List some available applications"""
        apps = list(self.app_cache.keys())[:20]  # First 20 apps
        print("\n📱 Some available applications:")
        for app in apps:
            print(f"   • {app}")
        self.speak(f"I found {len(self.app_cache)} applications. Check the console for a list.")
    
    def process_command(self, command):
        """Process voice command"""
        if not command:
            return True
        
        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # List available apps
        elif 'list apps' in command or 'show apps' in command or 'what apps' in command:
            self.list_apps()
        
        # Open applications or websites
        elif 'open' in command:
            # Remove 'open' and get the app name
            app_name = command.replace('open', '').strip()
            
            # Check if it's a common website
            common_sites = ['youtube', 'google', 'gmail', 'facebook', 'instagram', 
                          'twitter', 'linkedin', 'github', 'reddit', 'amazon', 'netflix']
            
            if any(site in app_name for site in common_sites):
                for site in common_sites:
                    if site in app_name:
                        self.open_website(site)
                        return True
            
            # Try to open as application
            if app_name:
                self.open_application(app_name)
            else:
                self.speak("Please specify what to open")
        
        # YouTube song/video search
        elif ('play' in command or 'search' in command) and 'youtube' in command:
            query = command.replace('play', '').replace('search', '').replace('on youtube', '').replace('youtube', '').replace('song', '').strip()
            if query:
                self.play_song_youtube(query)
            else:
                self.speak("What would you like me to play on YouTube?")
        
        # Direct song play command
        elif 'play' in command and ('song' in command or 'music' in command):
            query = command.replace('play', '').replace('song', '').replace('music', '').strip()
            if query:
                self.play_song_youtube(query)
            else:
                self.speak("Which song would you like me to play?")
        
        # Google search
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            if query:
                self.google_search(query)
            else:
                self.speak("What would you like me to search for?")
        
        # Close applications
        elif 'close' in command:
            app_name = command.replace('close', '').strip()
            if app_name:
                self.close_application(app_name)
            else:
                self.speak("Please specify which application to close")
        
        # Volume control
        elif 'volume' in command:
            if 'up' in command or 'increase' in command:
                self.volume_control("up")
            elif 'down' in command or 'decrease' in command:
                self.volume_control("down")
            elif 'mute' in command:
                self.volume_control("mute")
        
        # Screenshot
        elif 'screenshot' in command or 'capture screen' in command:
            self.take_screenshot()
        
        # Time
        elif 'time' in command:
            self.get_time()
        
        # Date
        elif 'date' in command or 'today' in command:
            self.get_date()
        
        # Help
        elif 'help' in command or 'what can you do' in command:
            self.speak("I can open ANY application on your computer! "
                      "Just say 'open' followed by the app name. "
                      "I can also play songs on YouTube, search Google, control volume, "
                      "take screenshots, and much more. Say 'list apps' to see available applications.")
        
        else:
            self.speak("I'm not sure how to help with that. Say 'help' for available commands.")
        
        return True
    
    def run(self):
        """Main loop"""
        self.speak("Hello, how can I help you?")
        
        while True:
            command = self.listen()
            if not self.process_command(command):
                break

if __name__ == "__main__":
    print("=" * 70)
    print("   🎙️  UNIVERSAL VOICE ASSISTANT - ALL APPS ACCESS  🎙️")
    print("=" * 70)
    print("\n✨ This assistant can open ANY application on your computer!\n")
    print("📋 Available Commands:\n")
    print("🚀 OPEN ANY APP:")
    print("   • 'open [any app name]' - Works with ALL installed apps!")
    print("   • 'open chrome', 'open spotify', 'open steam', 'open discord'")
    print("   • 'open visual studio', 'open photoshop', 'open word'")
    print("   • 'list apps' - See available applications")
    print("\n🌐 WEBSITES:")
    print("   • 'open youtube/google/gmail/facebook/instagram'")
    print("\n🎵 MUSIC & VIDEOS:")
    print("   • 'play [song name] on youtube'")
    print("   • 'play despacito', 'search cat videos on youtube'")
    print("\n🔍 SEARCH:")
    print("   • 'search [anything]' or 'google [query]'")
    print("\n🎛️  SYSTEM:")
    print("   • 'volume up/down/mute'")
    print("   • 'take screenshot'")
    print("   • 'close [app name]'")
    print("   • 'what's the time/date'")
    print("\n❌ EXIT:")
    print("   • 'exit' or 'quit' or 'goodbye'")
    print("\n" + "=" * 70)
    print("🎤 Starting assistant...\n")
    
    try:
        assistant = UniversalVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n❌ Assistant stopped by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📦 Please install required packages:")
        print("pip install SpeechRecognition pyttsx3 pyaudio pyautogui")
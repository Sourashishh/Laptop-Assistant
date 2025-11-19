# Universal Voice-Activated Laptop Assistant

A powerful Python-based voice assistant that can control your entire computer using voice commands. Open any application, play music on YouTube, search the web, and manage your system - all hands-free!

---

## Features

### Universal App Control
- Open ANY application installed on your PC
- Automatically scans your system for all apps
- Works with Spotify, Discord, Chrome, Steam, VS Code, and more!

### YouTube Integration
- Play songs directly: "play despacito on youtube"
- Auto-plays the first video from search results
- Search any video or music

### Web Control
- Open websites: Gmail, Facebook, Instagram, Twitter, etc.
- Google search with voice commands

### System Controls
- Volume control (up/down/mute)
- Take screenshots
- Close applications
- Get time and date

### Natural Language
- Understands casual commands
- Fuzzy app name matching
- Voice feedback for all actions

---

## Installation

### 1. Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Working microphone
- Internet connection (for speech recognition)

### 2. Install Dependencies

```bash
pip install SpeechRecognition pyttsx3 pyaudio pyautogui
```

#### For Windows Users:
If pyaudio installation fails, use:
```bash
pip install pipwin
pipwin install pyaudio
```

#### For macOS Users:
```bash
brew install portaudio
pip install pyaudio
```

#### For Linux Users:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

## Quick Start

1. Download the main.py file
2. Install dependencies (see above)
3. Run the assistant:
   ```bash
   python main.py
   ```
4. Wait for it to scan your applications (takes 10-30 seconds)
5. Start talking! Say "Hello" or any command

---

## Usage and Commands

### Opening Applications

```
"open chrome"
"open spotify"
"open discord"
"open visual studio code"
"open microsoft word"
"open steam"
"open notepad"
```

Tip: Just say "open" + the app name! The assistant will find it.

---

### Opening Websites

```
"open youtube"
"open google"
"open gmail"
"open facebook"
"open instagram"
"open twitter"
"open linkedin"
"open github"
```

---

### Playing Music/Videos

```
"play despacito on youtube"
"play imagine dragons song"
"play bohemian rhapsody"
"play shape of you on youtube"
"search funny cat videos on youtube"
```

Note: The assistant opens YouTube and automatically clicks the first video!

---

### Web Search

```
"search python tutorials"
"google machine learning"
"search how to make pizza"
```

---

### System Controls

```
"volume up"
"volume down"
"mute volume"
"take screenshot"
"close chrome"
"close spotify"
```

---

### Information

```
"what's the time"
"what's the date"
"what day is today"
```

---

### Utility Commands

```
"list apps" - See all detected applications
"help" - Get list of available commands
"exit" / "quit" / "goodbye" - Close the assistant
```

---

## Troubleshooting

### "Could not find [app] on your system"

Solutions:
1. Say the full application name (e.g., "visual studio code" not "vs code")
2. Check if the app was detected: say "list apps"
3. The app might be named differently - try variations
4. Restart the assistant to rescan applications

---

### Microphone Not Working

Solutions:
1. Check if your microphone is plugged in
2. Test microphone in other apps (Windows Voice Recorder, etc.)
3. Grant microphone permissions to Python
4. Try adjusting duration in code from 0.5 to 1.0:
   ```python
   self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
   ```

---

### Speech Recognition Issues

Solutions:
1. Speak clearly and at normal pace
2. Reduce background noise
3. Check your internet connection (Google Speech API requires internet)
4. Adjust microphone sensitivity in system settings

---

### YouTube Videos Not Auto-Playing

Solutions:
1. Increase wait time if you have slow internet:
   ```python
   time.sleep(6)  # Change from 4 to 6 seconds
   ```
2. Make sure YouTube loads completely before automation kicks in
3. Manually click the video if auto-play fails

---

### Apps Like Spotify Not Opening

Solutions:
1. Check the startup messages - see if Spotify was detected
2. Reinstall the app if it's not in a standard location
3. Try the full app name: "open spotify" (not "open spot")
4. Manually add the path in the code if needed

---

## Customization

### Change Voice Speed
Edit line in __init__ method:
```python
self.engine.setProperty('rate', 160)  # Lower = slower, Higher = faster
```

### Change Voice Volume
```python
self.engine.setProperty('volume', 0.9)  # 0.0 to 1.0
```

### Adjust Listening Timeout
```python
audio = self.recognizer.listen(source, timeout=5)  
```

### Add More Websites
Edit the websites dictionary in open_website() method:
```python
websites = {
    'youtube': 'https://www.youtube.com',
    'yoursite': 'https://www.yoursite.com', 
}
```

---

## Project Structure

```
main.py                     # Main assistant code
├── UniversalVoiceAssistant # Main class
│   ├── __init__()         # Initialize components
│   ├── scan_system_apps() # Find all installed apps
│   ├── listen()           # Voice input
│   ├── speak()            # Voice output
│   ├── open_application() # Open any app
│   ├── play_song_youtube()# YouTube playback
│   └── process_command()  # Command handler
```

---

## Technical Details

### Technologies Used:
- SpeechRecognition - Google Speech API for voice-to-text
- pyttsx3 - Text-to-speech engine
- pyautogui - Keyboard/mouse automation
- subprocess - Process management
- webbrowser - Web control
- winreg - Windows Registry access (Windows only)

### Supported Platforms:
- Windows 10/11 (Best support)
- macOS (Good support)
- Linux (Basic support)

---

## Example Workflow

```
1. Start assistant: python main.py
2. Wait for: "Hello, how can I help you?"
3. Say: "open spotify"
4. Assistant: "Opening spotify" (Spotify launches)
5. Say: "play lose yourself on youtube"
6. Assistant: "Playing lose yourself on YouTube" (Opens and plays video)
7. Say: "volume up"
8. Assistant: "Volume increased"
9. Say: "what's the time"
10. Assistant: "The time is 3:45 PM"
11. Say: "goodbye"
12. Assistant: "Goodbye! Have a great day!" (Exits)
```

---

## Known Issues

1. YouTube auto-play may not work if the page loads slowly
2. App detection might miss portable/non-standard installations
3. Speech recognition requires internet connection
4. Some apps may require administrator privileges

---

## Future Improvements

- Offline speech recognition
- Support for Spotify/music player controls
- Email sending capability
- Calendar integration
- Smart home control
- Custom wake word (like "Hey Assistant")
- Multi-language support
- GUI interface

---

## License

This project is open-source and free to use. Feel free to modify and customize it for your needs!

---

## Contributing

Found a bug? Have a feature request? Feel free to:
1. Report issues
2. Suggest improvements
3. Share your customizations

---

## Disclaimer

This assistant requires microphone access and can control your computer. Use responsibly and ensure you understand the code before running it.

---

## Tips for Best Experience

1. Speak clearly - Enunciate your words
2. Reduce noise - Use in a quiet environment
3. Wait for prompt - Let the assistant finish speaking before next command
4. Be specific - Use full app names when possible
5. Practice - The more you use it, the better you'll get!

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Read error messages carefully
3. Verify all dependencies are installed
4. Check if your microphone works in other apps

---

## Enjoy Your Voice Assistant!

Now you can control your entire computer hands-free! Say goodbye to clicking and typing - just speak your commands and let the assistant do the work!

Start commanding: `python main.py`

---

Made with love for productivity and accessibility
By Sourashish Majumdar
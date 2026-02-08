import signatures
import time
import threading
import sys
from colorama import Fore
from mutagen.mp3 import MP3
from pygame import mixer

mixer.init()

# ------
SONG_NAME = "The Third Sanctuary" # Name of the song
UPDATE_SETTING = "DYNAMIC" # 'MANUAL': Updates depending on Update_Frequency; 'DYNAMIC': Updates dynamically based on BPM/Beat
SOUNDS_ENABLED = True # Enable / Disable SFX

Update_Frequency = 0.05 # (UPDATE_SETTING must be 'MANUAL'); How often the display updates; lower numbers are more accurate, but take more CPU (0.05-0.2 recomended)
# ------

song_path = f"music/{SONG_NAME.lower()}.mp3"
bpm = signatures.get(SONG_NAME, "bpm")[0]
time_signatures = signatures.get(SONG_NAME, "signatures")[0]
total_length = MP3(song_path).info.length

mins, secs = divmod(total_length, 60)
mins, secs = int(mins), int(secs)

current_min = 0
current_sec = 0
current_ms = 0

total_beats = total_beats = sum(numerator for numerator, denominator in time_signatures)
current_beat = 1
current_beat_sig = 1

num, den = 0,0

beat_sfx = mixer.Sound("beat.wav")
end_beat_sfx = mixer.Sound("beat_end.wav")
mixer.music.load(song_path)

mixer.music.play()

def moveBack(amount):
    return "\033[F" * amount

def newLine(amount):
    return "\n" * amount

print(newLine(25))

def sendOutput():
    global current_min, current_sec, current_ms
    while True:
        if (current_ms >= total_length*1000) or (current_ms == -1):
            break
        
        current_ms = mixer.music.get_pos()
        current_min, current_sec = divmod(current_ms//1000, 60)
        current_min, current_sec = int(current_min), int(current_sec)
        print(f"""
              {moveBack(7)}
              |  {Fore.LIGHTCYAN_EX}Playing Song:{Fore.RESET}              
              |  {Fore.YELLOW}{SONG_NAME}{Fore.RESET} ({current_min:02d}:{current_sec:02d}/{mins:02d}:{secs:02d})              
              |  {Fore.GREEN}{bpm}BPM  {Fore.RED}{num}/{den}  {Fore.BLACK}({current_beat}/{total_beats}){Fore.RESET}              
              |              
              |     Beat {current_beat_sig}{Fore.BLACK}/{num}{Fore.RESET}         
              """
            , end="")
        time.sleep(Update_Frequency)

threading.Thread(target=sendOutput).start()

for numerator, denominator in time_signatures:
    num, den = numerator, denominator
    if (current_ms >= total_length*1000) or (current_ms == -1):
        break

    spb = 60 / bpm * (4 / denominator) # seconds per beat
    if UPDATE_SETTING == "DYNAMIC":
        Update_Frequency = spb
    for i in range(1, numerator + 1):
        current_beat_sig = i
        if SOUNDS_ENABLED:
            if i == 1: # first beat of the measure
                end_beat_sfx.play()
            else:
                beat_sfx.play()
        
        current_beat += 1
        time.sleep(spb)

sys.exit()
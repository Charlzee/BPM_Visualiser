import signatures
import time
import threading
from colorama import Fore
from mutagen.mp3 import MP3
from pygame import mixer, quit

mixer.init()
beat_sfx = mixer.Sound("beat.wav")
end_beat_sfx = mixer.Sound("beat_end.wav")
mixer.music.load("music.mp3")

song_name = "The Third Sanctuary"
bpm = signatures.get(song_name, "bpm")[0]
time_signatures = signatures.get(song_name, "signatures")[0]
total_length = MP3("music.mp3").info.length

mins, secs = divmod(total_length, 60)
mins, secs = int(mins), int(secs)

current_min = 0
current_sec = 0

total_beats = total_beats = sum(numerator for numerator, denominator in time_signatures)
current_beat = 1
current_beat_sig = 1

num, den = 0,0


mixer.music.play()

def moveBack(amount):
    return "\033[F" * amount

def newLine(amount):
    return "\n" * amount

print(newLine(25))

def sendOutput():
    global current_min, current_sec
    while mixer.music.get_busy():
        current_ms = mixer.music.get_pos()
        current_min, current_sec = divmod(current_ms//1000, 60)
        current_min, current_sec = int(current_min), int(current_sec)
        print(f"""
              {moveBack(7)}
              |  {Fore.LIGHTCYAN_EX}Playing Song:{Fore.RESET}              
              |  {Fore.YELLOW}{song_name}{Fore.RESET} {current_min:02d}:{current_sec:02d}/{mins:02d}:{secs:02d}              
              |  {Fore.GREEN}{bpm}BPM  {Fore.RED}{num}/{den}  {Fore.BLACK}({current_beat}/{total_beats}){Fore.RESET}              
              |              
              |     Beat {current_beat_sig}{Fore.BLACK}/{num}{Fore.RESET}              
              """
            , end="")
        time.sleep(0.05)

threading.Thread(target=sendOutput).start()

for numerator, denominator in time_signatures:
    num, den = numerator, denominator
    if not mixer.music.get_busy():
        break # music ended

    spb = 60 / bpm * (4 / denominator) # update seconds per beat
    for i in range(1, numerator + 1):
        current_beat_sig = i
        if i == 1: # first beat of the measure
            end_beat_sfx.play()
        else:
            beat_sfx.play()
        
        current_beat += 1
        time.sleep(spb)

mixer.quit()
quit()
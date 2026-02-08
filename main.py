import signatures
import time
from colorama import Fore
from pygame import mixer, quit

mixer.init()
beat_sfx = mixer.Sound("beat.wav")
end_beat_sfx = mixer.Sound("beat_end.wav")
mixer.music.load("music.mp3")

song_name = "The Third Sanctuary"
bpm = signatures.get(song_name, "bpm")[0]
time_signatures = signatures.get(song_name, "signatures")[0]

mixer.music.play()

def moveBack(amount):
    return "\033[F" * amount

def newLine(amount):
    return "\n" * amount

print(newLine(70))

for numerator, denominator in time_signatures:
    if not mixer.music.get_busy():
        break # music ended

    spb = 60 / bpm * (4 / denominator) # update seconds per beat
    for i in range(1, numerator + 1):
        print(f"""
              {moveBack(7)}
              |  {Fore.BLACK}Playing Song:{Fore.RESET}              
              |  {Fore.YELLOW}{song_name}{Fore.RESET}
              |  {Fore.GREEN}{bpm}BPM  {Fore.RED}{numerator}/{denominator}{Fore.RESET}              
              |              
              |     Beat {i}{Fore.BLACK}/{numerator}{Fore.RESET}              
              """
            , end="")
        
        if i == 1: # first beat of the measure
            end_beat_sfx.play()
        else:
            beat_sfx.play()
        
        time.sleep(spb)

mixer.quit()
quit()
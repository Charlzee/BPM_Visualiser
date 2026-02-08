import signatures
import time
from pygame import mixer, quit

mixer.init()
beat_sfx = mixer.Sound("beat.wav")
end_beat_sfx = mixer.Sound("beat_end.wav")
mixer.music.load("music.mp3")

bpm = 170
time_signatures = signatures.get("The Third Sanctuary")[0]

mixer.music.play()

for numerator, denominator in time_signatures:
    if not mixer.music.get_busy():
        break  # music ended

    spb = 60 / bpm * (4 / denominator)  # update seconds per beat
    for i in range(1, numerator + 1):
        print(f"Beat {i}     ", end="\r")
        
        if i == 1: # first beat of the measure
            end_beat_sfx.play()
        else:
            beat_sfx.play()
        
        time.sleep(spb)

mixer.quit()
quit()
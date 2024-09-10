#!/usr/bin/env python3
"""
PWM Tone Generator - Imperial March (Darth Vader's Theme)
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)  # Set duty cycle
    speaker.freq(frequency)  # Set frequency
    utime.sleep(duration)  # Play for 'duration' seconds
    quiet()  # Silence between notes


def quiet():
    speaker.duty_u16(0)


# Frequencies for the Imperial March (in Hz)
C4 = 261
D4 = 293
E4 = 329
F4 = 349
G4 = 392
A4 = 440
A4S = 466  # A#4 (A-sharp)
B4 = 493
C5 = 523
D5 = 587
E5 = 659  # E5 (higher octave)
F5 = 698  # F5 (higher octave)
G5 = 783
A5 = 880

# Duration constants
short = 0.3  # Short notes
longish = 0.6   # Long notes
extra_long = 0.9  # Extra-long notes
pause = 0.1  # Small pause between phrases

# Extended Imperial March notes and timings
imperial_march = [
    # Phrase 1: "Dah dah dah"
    (A4, short), (A4, short), (A4, short),  
    (F4, longish), (C5, short),  
    (A4, short), (F4, longish), (C5, short), (A4, extra_long),  
    
    # Phrase 2: "Dah dah dah, dah dah dah, dah!"
    (E5, short), (E5, short), (E5, short),  
    (F5, longish), (C5, short),  
    (A4S, short), (F4, longish), (C5, short), (A4, extra_long),
    
]



# Play the Imperial March
for note, dur in imperial_march:
    if note == 0:
        quiet()  # Rest
        utime.sleep(dur)
    else:
        playtone(note, dur)

# Turn off the PWM after playing
quiet()
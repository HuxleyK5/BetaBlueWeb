"""Optional cached procedural audio cues with silent fallback."""

from array import array
import io
import math
import wave

import pygame


class AudioManager:
    CUES = {
        "confirm": ((660, 0.07), (880, 0.08)),
        "cancel": ((330, 0.10),),
        "encounter": ((440, 0.08), (554, 0.08), (740, 0.12)),
        "battle": ((220, 0.08), (330, 0.08), (440, 0.12)),
        "capture": ((523, 0.08), (659, 0.08), (784, 0.16)),
        "quest": ((587, 0.08), (740, 0.08), (880, 0.18)),
        "error": ((180, 0.14),),
    }

    def __init__(self, master_volume=0.7, sfx_volume=0.8):
        self.master_volume = max(0.0, min(1.0, master_volume))
        self.sfx_volume = max(0.0, min(1.0, sfx_volume))
        self.enabled = False
        self._sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def play(self, cue):
        if not self.enabled or cue not in self.CUES or self.master_volume <= 0 or self.sfx_volume <= 0:
            return False
        if cue not in self._sounds:
            self._sounds[cue] = pygame.mixer.Sound(file=io.BytesIO(_wave_bytes(self.CUES[cue])))
        self._sounds[cue].set_volume(self.master_volume * self.sfx_volume)
        self._sounds[cue].play()
        return True

    def shutdown(self):
        if self.enabled:
            pygame.mixer.stop()


def _wave_bytes(notes, sample_rate=22050):
    samples = array("h")
    amplitude = 7000
    for frequency, duration in notes:
        count = int(sample_rate * duration)
        for index in range(count):
            envelope = min(1.0, index / 120) * min(1.0, (count - index) / 180)
            value = int(amplitude * envelope * math.sin(2 * math.pi * frequency * index / sample_rate))
            samples.extend((value, value))
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(sample_rate); wav.writeframes(samples.tobytes())
    return output.getvalue()

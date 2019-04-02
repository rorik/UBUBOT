from subprocess import Popen, run
from threading import Timer
from random import choice
from enum import Enum
from os import path

# Sound root
_root = path.dirname(path.abspath(__file__))

class Sounds(Enum):
    _ENABLE = "enable.s"
    _DISABLE = "disable.s"
    _RESET = "reset.s"
    SIREN = "siren.s"
    SYMPH9 = "symph9.s"
    PORTAL = "portal.s"
    PKMN_WILD_RB = "pokemon_b_w_rb.s"
    PKMN_WILD_RS = "pokemon_b_w_rs.s"
    PKMN_WILD_BW = "pokemon_b_w_bw.s"
    PKMN_TRNR_RB = "pokemon_b_t_rb.s"
    PKMN_TRNR_RS = "pokemon_b_t_rs.s"
    #PKMN_VICT_RB = "pokemon_v_rb.s"


class Player(object):
    def __init__(self):
        self._playing = None
    
    def _terminate(self):
        self._playing.terminate()
        self._playing = None
        self._run(Sounds._RESET.value)
    
    def _play(self, filename):
        self.stop()
        self._playing = Popen(path.join(_root, filename))
    
    def _run(self, filename):
        run(path.join(_root, filename))
    
    def play(self, sound, time=None):
        if not isinstance(sound, Sounds):
            raise TypeError("Expected sound (Player.Sounds)")
        self._play(sound.value)
        if time is not None:
            Timer(time, self._terminate)
    
    def stop(self):
        if self._playing is not None:
            self._terminate()

    def enable(self):
        self._run(Sounds._ENABLE.value)
    
    def disable(self):
        self._run(Sounds._DISABLE.value)
    
    def play_random(self, time=None):
        sound = choice([sound for sound in Sounds if not sound.name.startswith('_')])
        self.play(sound, time)
        return sound

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
__version__ = '1.0'
import logging
try:
    from pygame_macro import start_recording, stop_recording, is_recording, play_macro, stop_macro
except ImportError as e:
    logging.error(e)
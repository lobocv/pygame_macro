import json
import logging
import os
import pygame
import threading
import time

from pygame.constants import *

pygame_event_get = None
logger = None
start_time = None
STOP_MACRO = False

EVENT_ATTRIBUTES = {
                    QUIT             : ('type', ),
                    ACTIVEEVENT      : ('type', 'gain', 'state'),
                    KEYDOWN          : ('type', 'unicode', 'key', 'mod'),
                    KEYUP            : ('type', 'key', 'mod'),
                    MOUSEMOTION      : ('type', 'pos', 'rel', 'buttons'),
                    MOUSEBUTTONUP    : ('type', 'pos', 'button'),
                    MOUSEBUTTONDOWN  : ('type', 'pos', 'button'),
                    JOYAXISMOTION    : ('type', 'joy', 'axis', 'value'),
                    JOYBALLMOTION    : ('type', 'joy', 'ball', 'rel'),
                    JOYHATMOTION     : ('type', 'joy', 'hat', 'value'),
                    JOYBUTTONUP      : ('type', 'joy', 'button'),
                    JOYBUTTONDOWN    : ('type', 'joy', 'button'),
                    VIDEORESIZE      : ('type', 'size', 'w', 'h'),
                    VIDEOEXPOSE      : ('type',),
                    USEREVENT        : ('type', 'code',)
                    }


def get_events(*args):
    """
    Wrapper to the pygame.event.get() function which records all events to a file (macro)
    :param args: arguments to pygame.event.get()
    :return: pygame events
    """
    global start_time, EVENT_ATTRIBUTES

    for e in pygame_event_get(*args):
        delta_t = time.time() - start_time
        line = {f: getattr(e, f) for f in EVENT_ATTRIBUTES[e.type]}
        line['time'] = delta_t
        logger.info(json.dumps(line))
        yield e


def is_recording():
    return pygame.event.get != pygame_event_get and pygame_event_get is not None


def start_recording(path):
    """
    Start recording a new macro. Overwrites path if it exists
    :param path:
    :return:
    """
    global pygame_event_get, logger, start_time
    if os.path.isfile(path):
        with open(path, 'w'):
            pass
    start_time = time.time()
    if logger is None:
        logger = logging.getLogger('pygame_macro')
        logger.setLevel(logging.INFO)
        logger.propagate = False
        rfh = logging.FileHandler(path)
        logger.addHandler(rfh)

    pygame_event_get = pygame.event.get
    pygame.event.get = get_events


def stop_recording():
    """
    Stop recording the macro.
    """
    if is_recording():
        pygame.event.get = pygame_event_get


def play_macro(path):
    """
    Start a recorded macro.
    :param path:
    :return:
    """
    global STOP_MACRO
    STOP_MACRO = False
    if os.path.isfile(path):
        t = threading.Thread(target=_queue_events, args=(path,))
        t.start()


def stop_macro():
    global STOP_MACRO
    STOP_MACRO = True


def _queue_events(path):
    """
    Reads events from a recorded macro and posts them to the pygame event queue.
    :param path: path to macro
    """
    Event = pygame.event.Event
    post = pygame.event.post
    t0 = time.time()
    with open(path, 'r') as f:
        for l in f:
            if STOP_MACRO:
                return
            elapsed_time = time.time() - t0
            line = json.loads(l)
            t = float(line['time'])
            e = Event(line['type'], **line)
            while elapsed_time < t:
                time.sleep(0.01)
                elapsed_time = time.time() - t0
            while 1:
                try:
                    post(e)
                    break
                except pygame.error:
                    time.sleep(0.25)


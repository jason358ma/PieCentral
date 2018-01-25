import time
import threading
import collections
import heapq
import LCM
from Utils import *

class Timer:
    """
    This class should spawn another thread that will keep track of a target time
    and compare it to the current system time in order to see how much time is left
    """
    class busyThread(threading.Thread):
        '''
        Subclass that is the actual thread that will be running.
        There will only be one for the entire class.
        '''
        def __init__(self, queue):
            super().__init__()
            self.queue = queue
            self.stop = threading.Event()

        def run(self):
            '''
            When started, thread will run and process Timers in queue until manually stopped
            TODO: Add how to send message via LCM in the case of match timer
            '''
            while not self.stop.isSet():
                if not self.queue.empty() and self.queue[0].endTime < time.time():
                    Timer.queueLock.acquire()
                    event = heapq.heappop(self.queue)
                    if event.timer_type == TIMER_TYPES.MATCH:
                        LCM.lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.STAGE_TIMER_END)
                    if event.timer_type == TIMER_TYPES.BID:
                        LCM.lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.BID_TIMER_END)
                    event.active = False
                    Timer.queueLock.release()

        def join(self, timeout=None):
            '''Stops this thread. Must be called from different thread (Main Thread)'''
            super().join(timeout)
            self.stop.set()
            Timer.running = False

    eventQueue = []
    thread = busyThread(eventQueue)
    running = False
    queueLock = threading.Lock()

    def __init__(self, timer_type, goal_name=None):
        """
        timer_type - a Enum representing the type of timer that this is:
                        TIMER_TYPES.BID - represents a bid timer
                        TIMER_TYPES.MATCH - represents the time of the current
                                            stage in the match
                        TIMER_TYPES.COOLDOWN - represents a cooldown timer for
                                               the cooldown when a powerup
                                               cannot be applied
                        TIMER_TYPES.CODE_COOLDOWN - represents a cooldown timer
                                                    for a code
                        TIMER_TYPES.DURATION - represents a duration timer for
                                               a powerup
        """
        self.active = False
        self.timer_type = timer_type
        self.goal_name = goal_name
        self.endTime = None

    def start_timer(self, duration):
        """Starts a new timer with the duration (seconds) and sets timer to active.
           If Timer is already running, adds duration to Timer"""
        if self.active:
            Timer.queueLock.acquire()
            self.endTime += duration
            heapq.heapify(Timer.eventQueue)
            Timer.queueLock.release()
        else:
            if not Timer.running:
                Timer.running = True
                Timer.thread.start()
            Timer.queueLock.acquire()
            self.endTime = time.time() + duration
            heapq.heappush(Timer.eventQueue, self)
            self.active = True
            Timer.queueLock.release()


    def reset(self):
        """Stops the current timer (if any) and sets timer to inactive"""
        if self.active:
            Timer.queueLock.acquire()
            Timer.eventQueue.remove(self)
            heapq.heapify(Timer.eventQueue)
            self.active = False
            Timer.queueLock.release()

    def is_running(self):
        """Returns true if the timer is currently running"""
        return self.active

    def reset_all():
        #TODO
        pass

    ###########################################
    # Timer Comparison Methods
    ###########################################
    def __lt__(self, other):
        return self.endTime < other.endTime

    def __gt__(self, other):
        return self.endTime > other.endTime

    def __eq__(self, other):
        return self.endTime == other.endTime

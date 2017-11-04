import sys
import Goal
import random


class Shepherd:

    def __init__(self): # Don't think we need the matchNumber here.
        '''
        Initializes all of the state needed to maintain the current status of elements on the field
        '''

        #The following are elements that are expected to exist in every iteration of the game
        self.UI = UI()
        self.schedule = Web()
        self.match_timer = Timer()
        self.match_number = 1

        #The follwing are elements that are configured
        # specifically for the 2018 year game - Solar Scramble

        self.blue_powerup_timers = {'a': PowerupTimer(),
                                    'b': PowerupTimer(),
                                    'c': PowerupTimer(),
                                    'd': PowerupTimer(),
                                    'e': PowerupTimer()}
        self.gold_powerup_timers = {'a': PowerupTimer(),
                                    'b': PowerupTimer(),
                                    'c': PowerupTimer(),
                                    'd': PowerupTimer(),
                                    'e': PowerupTimer()}
        self.blue_decode_timers = PowerupTimer()
        self.gold_decode_timers = PowerupTimer()
        self.sensors = Sensors()
        self.score = {'blue': 0, 
                      'gold': 0}

        self.event_mapping = {
            "setup_match": setup_match,
            "start_auto": start_auto,
            "start_telop": start_telop,
            "start_next_stage": start_next_stage,
            "reset_match": reset_match,
            "reset_stage": reset_stage,
            "reset_lcm": reset_lcm,
            "end_match": end_match,
        }

        #self.scoreboard = Scoreboard(match_timer) # what even is a scoreboard
        #self.driverstation = Driverstation() # Make this into a wrapper class w/ the 4 diff driverstations?
        
        # BEGIN API SPECIFIC VARIABLES

        self.header_mapping = {} # Todo
        self.current_stage = 0

        self.alliances = {} # Todo
        self.goals = {'a': Goal(),'b': Goal(),'c': Goal(),'d': Goal(),'e': Goal()}

        self.event_queue = [] # Todo

        self.RFID_pool = []
        self.curr_RFID = {}

    # START API METHODS

    def generate_code():
        # Should be handled by codegen

    def check_code(code):
        # Should be handled by codegen

    def populate_RFID(file = 'RFIDs.txt'):
        '''
        Selects 6 random RFID codes from RFIDs.txt and populates curr_RFID
        with one code in each slot. Also prints out curr_RFID for debugging.

        Inputs: file: a string that points to a .txt file with one RFID code
        per line.
        '''
        RFIDs = open(file, 'r')
        all_codes = RFIDs.readlines()
        random_indices = random.sample(range(len(all_codes)-1), 6)

        self.curr_RFID = {
            '0Blue': all_codes[random_indices[0]],
            '2Blue': all_codes[random_indices[1]],
            'stealBlue': all_codes[random_indices[2]],
            '0Gold': all_codes[random_indices[3]],
            '2Gold': all_codes[random_indices[4]],
            'stealGold': all_codes[random_indices[5]]}

        print self.curr_RFID

    # END API METHODS



    # UI Commands
    # (Ideally, this stuff should be depricated and rewritten)

    def setup_match(self, matchNumber):
        #Assuming the UI/ctrl station will provide us with a match number arg
        self.match_number = matchNumber
        teams = self.schedule.getTeams(self.match_number)
        self.alliances= {'blue': Alliance(teams[0], teams[1]), 'gold': Alliance(teams[2], teams[3])}
        self.current_stage = 'NONE'
        self.timer = Timer()
        self.score = {'blue': 0, 
                      'gold': 0}
        broadcast_status("Set up match #" + str(self.match_number))

    def start_auto(self):
        self.current_stage = 'AUTO'
        self.match_timer.reset()
        self.set_driver_stations_mode("AUTO")
        # assuming autonomous means we operate independently of the driver station
        broadcast_status("Starting autonomous")
        self.match_timer.start("AUTO_TIME")

    def start_telop(self):
        self.current_stage = 'TELOP'
        self.match_timer.reset()
        self.set_driver_stations_mode("TELOP")
        broadcast_status("Starting teleop")
        self.match_timer.start("TELOP_TIME")

    def start_next_stage(self):
        if self.current_stage == 'NONE':
            self.start_auto()
        else if self.current_stage == 'AUTO':
            self.start_telop()
        else:
            self.end_match()

    def end_match(self):
        self.current_stage = 'NONE'
        self.set_driver_stations_mode("NONE")
        broadcast_status("Ending match")
        self.schedule.update_scores(self.score['blue'], self.score['gold'])
        # what else do we do?

    def reset_match(self):
        self.end_match()
        self.setup_match()

    def reset_stage(self):
        # probably need to reset score to prev state as well (rollback), something for the alliance to handle?
        # where do we even start

    def reset_lcm(self):
        # what happens here? can't we just force the lcm to do this itself?
        

    def set_driver_stations_mode(self, mode):
        if mode == "AUTO":
            #self.driverstation.blue.set_mode('AUTO')
        else if mode == "TELOP":
            #self.driverstation.blue.set_mode('TELOP')
        else:
            #self.driverstation.blue.set_mode('NONE')

    # Sensors
    def goal_scored(alliance, goal):
        # Look up pt value, add it using modify_pts
        goal_value = 2
        scored_goal = goals[goal]
        if scored_goal.alliance == alliance:
            modify_points(alliance, scored_goal.goal_value)

    # Because I think we may need a seperate method for teams' permenant
    # goals and bidding changes
    def modify_points(alliance, points):
        if (alliance == 'blue' || alliance == 'gold'):
            score[alliance] += points 
        self.scoreboard.update_scores(score['blue'], score['gold'])



'''
    Things to receive:
        UI_Commands from field control:
            Setup_Match
            Start_Auto
            Start_Telop
            Start_Next_Stage #added
            Reset_Match
            Reset_Stage
            reset_lcm (optional)
            End_Match #added
        Button_Commands from bidding station:
            Bid on [Goal X] from [Alliance A]
        FromSensors:
            Ball scored in [Goal X] on [Alliance A]
            Code received from [Goal X] on [Alliance A]
        FromTimers:
            WhatTimerItIs, CurrentTimeReamining
            ChangeMatchState (for MatchTimers)
            ChangeGoalState (for GoalTimers)
            ChangeMultiplierState (for GoalMultipliers)
        FromDriverStation:
            Robot State (connected, disconnected, teleop, auto)
'''
class PowerupTimer:
    def __init__(self):
        self.steal = Timer()
        self.double = Timer()    
        self.zero = Timer()

def main():
    shepherd = Shepherd()
    #uhhh

if __name__ == '__main__':
    main()


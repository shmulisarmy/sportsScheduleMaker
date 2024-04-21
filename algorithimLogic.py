class ScheduleMaker:
    """since it's not thread safe, it will kick you out if you try to create multiple schedules at once"""
    """code sample:
           sportOptions = ["baseketball", "football", "hockey", "volleyball"]
           main = ScheduleMaker([i for i in range(1, 9)], sportOptions)
           main.createScedule(3)

        _{func} as all functions exept createScedule are private and should only be accessed by createScedule
    """
    def __init__(self, teams, sportOptions):
        self.teams = teams
        self.teamsPlayed = {i: [] for i in teams}

        self.sportOptions = sportOptions
        self.sportsPlayed = {i: [] for i in teams}

        self.teamsPlayedThisRound = []
        self.whoPlayedWhothisRound = {}

        self.sportsUsed = []

        self.inAction = False


    def _playgame(self, team1, team2, sport):
        self.teamsPlayed[team1].append(team2)
        self.teamsPlayed[team2].append(team1)
        self.teamsPlayedThisRound.append(team1)
        self.teamsPlayedThisRound.append(team2)
        self.whoPlayedWhothisRound[team1] = team2
        self.whoPlayedWhothisRound[team2] = team1
        self.sportsPlayed[team1].append(sport)
        self.sportsPlayed[team2].append(sport)

        self.sportsUsed.append(sport)



    def _unplay(self, team1, team2, sport):
        self.teamsPlayed[team1].pop(self.teamsPlayed[team1].index(team2))
        self.teamsPlayed[team2].pop(self.teamsPlayed[team2].index(team1))
        self.teamsPlayedThisRound.pop(self.teamsPlayedThisRound.index(team1))
        self.teamsPlayedThisRound.pop(self.teamsPlayedThisRound.index(team2))
        self.whoPlayedWhothisRound[team1] = False
        self.whoPlayedWhothisRound[team2] = False
        self.sportsPlayed[team1].pop(self.sportsPlayed[team1].index(sport))
        self.sportsPlayed[team2].pop(self.sportsPlayed[team2].index(sport))
        
        self.sportsUsed.pop(self.sportsUsed.index(sport))
        


    def _pairTeamsUp(self):
        if len(self.teamsPlayedThisRound) == len(self.teams):
            return True
        for team1 in self.teams:
            if team1 in self.teamsPlayedThisRound:
                continue
            for team2 in self.teams:
                if team1 == team2:
                    continue
                if team2 in self.teamsPlayedThisRound:
                    continue
                if team1 in self.teamsPlayed[team2] or team2 in self.teamsPlayed[team1]:
                    continue
                sportsNotPlayed = list(set(self.sportOptions) - set(self.sportsPlayed[team1]) - set(self.sportsPlayed[team2]) - set(self.sportsUsed))
                if len(sportsNotPlayed) == 0:
                    continue
                if len(sportsNotPlayed) < 1:
                    continue
                chosenSport = sportsNotPlayed[0]
                self._playgame(team1, team2, chosenSport)
                if self._pairTeamsUp():
                    return True
                self._unplay(team1, team2, chosenSport)

        return False
    
    def _displaySchedule(self, rounds: int):
        for round in range(1, rounds+1):
            print("-------"*3, "round", round, "-------"*3)
            for team in self.teams:
                print(f"team {team} will play team {self.teamsPlayed[team][round-1]} in {self.sportsPlayed[team][round-1]}")
        



    def _playRound(self):
        self.teamsPlayedThisRound = []
        self.whoPlayedWhothisRound = {}
        pairTeams = self._pairTeamsUp()
        self.sportsUsed = []
        print(f"{self.sportsPlayed = }")
        return pairTeams


    def createScedule(self, activities: int) -> str:
        if self.inAction:
            return "cannot create schedule while in action"
        self.inAction = True
        for round in range(1, activities+1):
            if self._playRound():
                roundsCanPlay = round
                print(self.whoPlayedWhothisRound)

        self.inAction = False


        self._displaySchedule(roundsCanPlay)
        return f"{roundsCanPlay} rounds can be played"



sportOptions = ["baseketball", "football", "hockey", "volleyball"]
main = ScheduleMaker([i for i in range(1, 9)], sportOptions)
main.createScedule(3)
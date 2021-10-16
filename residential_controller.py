elevatorID = 1
floorRequestButtonID = 1
callButtonID = 1

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
       self.ID = _id
       self.status = "online"
       self.amountOfFloors = _amountOfFloors
       self.amountOfElevators = _amountOfElevators
       self.elevatorList = []
       self.callButtonList = []

       self.createElevators(_amountOfFloors,_amountOfElevators)
       self.createCallButtons(_amountOfFloors)

       #---------------------------------Methods--------------------------------------------
   
    def createCallButtons(self,_amountOfFloors):    # this method creates Callbuttons
        global callButtonID
        self.buttonFloor = 1
        self.callButton = 0
        for element in  range(_amountOfFloors):
            
            if self.buttonFloor< _amountOfFloors:
                self.callButton = CallButton(callButtonID, self.buttonFloor, 'up')
                self.callButtonList.append(self.callButton)
                callButtonID+=1
            if self.buttonFloor>1 :
                self.callButton = CallButton(callButtonID, self.buttonFloor, 'down')
                self.callButtonList.append(self.callButton)
                callButtonID+=1
            self.buttonFloor+=1

    def createElevators(self,_amountOfFloors,_amountOfElevators):  # this method creates elevators based on elevator class
        global elevatorID

        for elevatorindex in range(_amountOfElevators):
            elevator = Elevator(elevatorID,_amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID+=1

    
    def requestElevator(self, floor, direction):     # this method is the one that makes the elevators work, it call the logic the motion and the operation of the elevator
        elevator = self.findElevator(floor,direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        return elevator




    def findElevator(self,requestedFloor,requestedDirection): # this method asigns a score depending on the condition of the elevator, the smaller the better
        bestElevator = {}
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = []


        for elevator in self.elevatorList:
            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1,elevator,bestScore,referenceGap,bestElevator,requestedFloor)
            
            elif requestedFloor >elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                 bestElevatorInformations = self.checkIfElevatorIsBetter(2,elevator,bestScore,referenceGap,bestElevator,requestedFloor)
            
            elif requestedFloor<elevator.currentFloor and elevator.direction == "down" and requestedDirection == elevator.direction:
                 bestElevatorInformations = self.checkIfElevatorIsBetter(2,elevator,bestScore,referenceGap,bestElevator,requestedFloor)

            elif elevator.status == 'idle':
                 bestElevatorInformations = self.checkIfElevatorIsBetter(3,elevator,bestScore,referenceGap,bestElevator,requestedFloor)
            
            else: bestElevatorInformations = self.checkIfElevatorIsBetter(4,elevator,bestScore,referenceGap,bestElevator,requestedFloor)

            bestElevator = bestElevatorInformations[0]
            bestScore = bestElevatorInformations[1]
            referenceGap = bestElevatorInformations[2]

        return bestElevator
    
    def checkIfElevatorIsBetter(self,scoreToCheck,newElevator,bestScore,referenceGap,bestElevator,floor):  # this method is the one that checks which elevator is better based on score
        if scoreToCheck<bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap>gap:
                bestElevator = newElevator
                referenceGap = gap

        bestElevatorInformations = [bestElevator,bestScore,referenceGap]
        return bestElevatorInformations



        





class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 0
        self.direction = None
        self.door =  Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []

        self.createFloorRequestButtons(_amountOfFloors)

#---------------------------------------------Methods---------------------------------------
   
    def createFloorRequestButtons(self,_amountOfFloors): #method create FloorRequestButtons
        global floorRequestButtonID
        buttonFloor = 1
        for element in range(_amountOfFloors):
            floorRequestButton =  FloorRequestButton(floorRequestButtonID,buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor+=1
            floorRequestButtonID+=1

            
    def requestFloor(self,floor): # this method make the logic of the elevator, it moves it operate its doors...
        self.floorRequestList.append(floor)
        self.move()
        self.operateDoors()

    def move(self):  # this is the method that makes the elevator move
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status ='moving'
            if self.currentFloor<destination:
                self.direction = 'up'
                self.sortFloorList()
                while self.currentFloor<destination:
                    self.currentFloor+=1
                    self.screenDisplay = self.currentFloor
            
            elif self.currentFloor>destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor>destination:
                    self.currentFloor-=1
                    self.screenDisplay = self.currentFloor

            self.status = 'stopped'
            self.floorRequestList.pop(0)

        self.status = 'idle'

    def sortFloorList(self):  # this is a method that sorts the floors for the floorRequestList
        if self.direction =='up':
            self.floorRequestList.sort()

        else: self.floorRequestList.sort(reverse = True)

    def operateDoors(self):   # this is method to operate doors, open close...
        overweight = False
        doorIsObstructed = False
        self.door.status == "open"
        if not overweight:
            self.door.status == "closing"
            if not doorIsObstructed:
                self.door.status == "closed"
            else: self.door.status == "opened" 

        else:
            while overweight:
                self.alarm()


    def alarm(self):  # not really a method, just for the sake of creating it so we call call it above
        alarm = 4






    


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status= ''
        self.floor = _floor
        self.direction = _direction


class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = 'OFF'
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = ''


class floor:
    ffff=3
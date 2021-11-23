# Amirhosseein Eskini & AmirReza Elahi

from random import randint
from sys import platform
from os import system
from time import sleep
from typing import List
from terminaltables import SingleTable

correctness = False

while not correctness:
    size = input("Enter room size: (size must be a number and bigger than 1)")
    if ((size.isdigit()) and (int(size) > 1)):
        size = int(size)
        correctness = True
    else:
        print("Please enter a correct number.")

state = {
    "status": "Moving...",
    "clearCommand": "cls" if platform == "win32" else "clear",
    "changeRowTo": "down",
    "canChangeRow": True,
    "goRight": True,
    "boxes": [],
    "canvas": "",
    "agentLocation": [],
    "checkRooms": []
}

def showInTable(rooms: list):
    table_instance = SingleTable(rooms)
    table_instance.outer_border = True
    table_instance.inner_heading_row_border = False
    table_instance.inner_column_border = True
    table_instance.inner_row_border = True
    print(table_instance.table)

def initialCheckRooms() -> list:
    global size
    array = []
    for i in range(size):
        array.append([])
        for _ in range(size):
            array[i].append(0)
    return array

def isCheckedAllRooms() -> bool:
    global size
    array = state["checkRooms"]
    flag = 1
    for i in range(size):
        for j in range(size):
            item = array[i][j]
            flag = item * flag
    return flag == 1

def makeBoxes(boxesStatus: list = None) -> list:
    global size
    boxes = []
    for i in range(size):
        boxes.append([])
        for j in range(size):
            boxes[i].append(randint(0, 1))
    return boxes

def showRooms():
    state["boxes"] = makeBoxes() if state["boxes"] == [] else state["boxes"]
    boxes = state["boxes"]
    rooms = []
    counter = 1
    for i in range(len(boxes)):
        rooms.append([])
        for _ in range(len(boxes)):
            rooms[i].append(str(counter))
            counter += 1

    showInTable(rooms)

def setVacuumLocation() -> list:
    global size
    correctness = False
    showRooms()
    
    while not correctness:
        place = input("choose a room please: ")
        if place.isdigit():
            place = int(place)
            if (place <= (size*size)):
                row = int(place % size)
                if row == 0 :
                    row = int(place/size) - 1
                else:
                    row = int(place/size)

                index = int(place % size)
                if index == 0:
                    index = size - 1
                else: 
                    index -= 1

                correctness = True
                return [row, index]
            else :
                print("❌ out of range")
        else:
            print("Please enter a correct input!")

def makeCanvas(boxes: list, agentLocation: list) -> list:
    global state
    canvas = []
    for i in range(len(boxes)):
        canvas.append([])
        for j in range(len(boxes[i])):
            canvas[i].append(               
                 "🧹"
                if i == agentLocation[0] and j == agentLocation[1]
                else "🦠"
                if boxes[i][j] == 1
                else "🧻"
            )
    return canvas

def moveAgent(currentLocation: list = None) -> list:
    global state
    if currentLocation == []:
        newLocation = setVacuumLocation()
    else:
        newLocation = [currentLocation[0], currentLocation[1]]
        state["checkRooms"][newLocation[0]][newLocation[1]] = 1

        if currentLocation[0] == 0:
            state["changeRowTo"] = "down"
        elif currentLocation[0] == (size - 1):
            state["changeRowTo"] = "up"

        # move the vacuum a row down from the right corner
        if currentLocation[1] == (size - 1) and state["canChangeRow"] == True:
            if state["changeRowTo"] == "up":
                newLocation[0] = currentLocation[0] - 1
            else:
                newLocation[0] = currentLocation[0] + 1
            newLocation[1] = currentLocation[1]
            state["canChangeRow"] = False
            state["goRight"] = False
        # move the vacuum a row down from the left corner
        elif currentLocation[1] == 0 and state["canChangeRow"] == True:
            if state["changeRowTo"] == "up":
                newLocation[0] = currentLocation[0] - 1
            else:
                newLocation[0] = currentLocation[0] + 1
            newLocation[1] = currentLocation[1]
            state["canChangeRow"] = False
            state["goRight"] = True
        # move the vacuum an index to right
        elif currentLocation[1] < (size - 1) and state["goRight"] == True:
            newLocation[0] = currentLocation[0]
            newLocation[1] = currentLocation[1] + 1
            state["canChangeRow"] = True
        # move the vacuum an index to left
        elif currentLocation[1] > 0 and state["goRight"] == False:
            newLocation[0] = currentLocation[0]
            newLocation[1] = currentLocation[1] - 1
            state["canChangeRow"] = True

    return newLocation


def changeStatus(currentStatus: str, boxesStatus: list, agentLocation: list) -> str:
    if currentStatus != "Finished.":
        if currentStatus == "Moving...":
            newStatus = "Checking..."
        elif currentStatus == "Checking...":
            if boxesStatus[agentLocation[0]][agentLocation[1]] == 1:
                newStatus = "Cleaning..."
            else:
                newStatus = "Moving..."
        elif currentStatus == "Cleaning...":
            boxesStatus[agentLocation[0]][agentLocation[1]] = 0
            newStatus = "Moving..."
    else:
        newStatus = currentStatus
    return newStatus


def action() -> None:
    global state
    sleep(1)
    system(state["clearCommand"])
    state["agentLocation"] = (
        moveAgent(state["agentLocation"])
        if state["status"] == "Moving..."
        else state["agentLocation"]
    )
    state["boxes"] = makeBoxes() if state["boxes"] == [] else state["boxes"]
    canvas = makeCanvas(state["boxes"], state["agentLocation"])

    print("Room size: " + str(size) + "x" + str(size))
    showInTable(canvas)
    print("Status: " + state["status"], sep="\n")

    state["status"] = changeStatus(
        state["status"], state["boxes"], state["agentLocation"]
    )

def start(unlimitedMovement: bool):
    if unlimitedMovement:
        while True:
            action()
    else:
        while isCheckedAllRooms() == False:
            action()

def initialize() -> None:
    global state
    state["checkRooms"] = initialCheckRooms()
    start(False)

initialize()

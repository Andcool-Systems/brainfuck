import sys
import json
import os

#------------------Имя файла-------------------------------
filename = "main.bf"
for i, param in enumerate(sys.argv):
    if i == 1: 
        filename = str(param)
        if not filename.split(".")[-1] in ["b", "bf"]:
            print(f"File '{filename}' is not a brainfuck script")
            sys.exit()
#------------------Парсим аргументы------------------------
if not os.path.isfile("params.json"):
    params = {
        "memorySize": 30000, 
        "memoryManagement": "OFF" #OFF/AUTO/JUMP
        }

    json_object = json.dumps(params, indent=2)
 
    with open(f"params.json", "w") as outfile:
        outfile.write(json_object)
else:
    with open(f'params.json', 'r') as openfile:
        params = json.load(openfile)


#-------------------Открываем-------------------------------
try:
    mainFile = open(str(filename), "r", encoding="ascii")
except FileNotFoundError:
    print("No such file or directory")
    sys.exit()
scriptMid = mainFile.read()
script = ''.join(char for char in scriptMid if char in "><+-.*,[]")
#---------------------------------------------------------


memory = [0] * (1 if params["memoryManagement"] == "AUTO" else int(params["memorySize"]))
pointer = 0
globalInterpreter = 0


#---------------------------------------------------------
opened = []
blocksOfCode = {}
for i, char in enumerate(script):
    if char == "[":
        opened.append(i)
    if char == "]":
        blocksOfCode[i] = opened[-1]
        startIndex = opened.pop()
        blocksOfCode[startIndex] = i
#---------------------------------------------------------


while globalInterpreter < len(script):
    char = script[globalInterpreter]
    try:
        if char == ">": 
            pointer += 1
            if params["memoryManagement"] == "AUTO":
                while pointer > len(memory) - 1:
                    memory.append(0)
            elif params["memoryManagement"] == "JUMP":
                if pointer > len(memory) - 1: pointer = 0
        if char == "<": 
            pointer -= 1
            if params["memoryManagement"] == "JUMP":
                if pointer < 0: pointer = len(memory) - 1
        if char == "+": memory[pointer] += 1
        if char == "-": memory[pointer] -= 1
        if char == ".": print(chr(memory[pointer]), end="")
        if char == "*": print(memory[pointer], end="")
        if char == ",": 
            sym = input("Input=")
            memory[pointer] = int(sym) if sym else 0
        if char == "[": 
            if memory[pointer] == 0: globalInterpreter = blocksOfCode[globalInterpreter]
        if char == "]": 
            if memory[pointer] != 0: globalInterpreter = blocksOfCode[globalInterpreter]
    except IndexError: 
        print(f'\n\nAllocated memory overflow on operator "{char}" on index {globalInterpreter}\nMemory index {pointer} on max {len(memory)-1}')
        break
    globalInterpreter += 1

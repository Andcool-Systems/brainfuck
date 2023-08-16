import sys
import json
import os
import utils

#------------------Имя файла-------------------------------
filename = "file.bf"
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
        "memoryManagement": "OFF", #OFF/AUTO/JUMP
        "type": "CLASSIC" #CLASSIC/ADVANCED
        }

    json_object = json.dumps(params, indent=2)
    try:
        with open(f"params.json", "w") as outfile:
            outfile.write(json_object)
    except IOError as e:
        # Обработка исключения IOError (включая [Errno 30] Read-only file system)
        if e.errno == 30:
            print("Error: The file system is read-only.")
        else:
            print(f"An I/O error has occurred: {e}")
else:
    with open(f'params.json', 'r') as openfile:
        params = json.load(openfile)


#-------------------Открываем-------------------------------
try:
    mainFile = open(str(filename), "r", encoding="utf-8")
except FileNotFoundError:
    print("No such file or directory")
    sys.exit()
scriptMid = mainFile.read()
script = utils.formatCode(scriptMid)
#---------------------------------------------------------

memory = [0] * (1 if params["memoryManagement"] == "AUTO" else int(params["memorySize"]))
pointer = 0
globalInterpreter = 0

#---------------------------------------------------------
blocksOfCode, portals = utils.init(script)
clipboard = 0
#---------------------------------------------------------
while globalInterpreter < len(script):
    char = script[globalInterpreter]
    lastChar = script[globalInterpreter - 1] if globalInterpreter > 1 else ""
    nextChar = script[globalInterpreter + 1] if globalInterpreter < len(script) - 1 else ""

    try:
        match char:
            case ">": 
                pointer += 1
                if params["memoryManagement"] == "AUTO":
                    while pointer > len(memory) - 1:
                        memory.append(0)
                        if len(memory) > int(params["memorySize"]) and int(params["memorySize"]) != -1:
                            print(f'\n\nUnable to allocate memory: The allocated memory limit has been reached.\nTo remove the limit, set the "memorySize" parameter to -1')
                            sys.exit()
                elif params["memoryManagement"] == "JUMP":
                    if pointer > len(memory) - 1: pointer = 0
            case "<": 
                pointer -= 1
                if params["memoryManagement"] == "JUMP":
                    if pointer < 0: pointer = len(memory) - 1
            case "+": 
                memory[pointer] += 1
                if params["type"] == "CLASSIC" and memory[pointer] > 255: memory[pointer] = 0
            case "-": 
                memory[pointer] -= 1
                if params["type"] == "CLASSIC" and memory[pointer] < 0: memory[pointer] = 255
            case ".":
                try: print((chr(memory[pointer]) if lastChar != "*" else memory[pointer]), end="")
                except ValueError: 
                    print(f"\n\nAttempt to display incorrect unicode {memory[pointer]} at position {globalInterpreter + 2}")
                    sys.exit()
            case ",": 
                sym = input("Input=")
                memory[pointer] = (int(sym) if sym else 0) if lastChar != "*" else (ord(int(sym) if sym else 0))
            case "[": 
                if memory[pointer] == 0: globalInterpreter = blocksOfCode[globalInterpreter]
            case "]": 
                if memory[pointer] != 0: globalInterpreter = blocksOfCode[globalInterpreter]
            case "c": clipboard = memory[pointer]
            case "p": memory[pointer] = clipboard
            case "'": print("   ", end="")
            case '"': print("")
            case "g": 
                try: globalInterpreter = portals[nextChar]
                except KeyError: 
                    print(f'\n\nCannot find goto exit named "{nextChar}"')
                    sys.exit()
            case "0": memory[pointer] = 0
    except IndexError: 
        print(f'\n\nAllocated memory overflow on operator "{char}" on index {globalInterpreter + 2}\nMemory index {pointer} on max {len(memory)-1}\nSet memoryManagement to "AUTO"')
        sys.exit()
    globalInterpreter += 1
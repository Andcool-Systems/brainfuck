import sys


def formatCode(code):
    ignore = [" ", "\n", "	", "	"]
    code1 = "".join([char for char in code if not char in ignore])
    splitted = code1.split("#")

    mem = None
    notOdd = False
    clearCodeList = []
    for i, element in enumerate(splitted):
        if element == "": mem = i
        elif mem == i - 1:
            mem = None
            notOdd = i % 2 == 0
        elif (i % 2 == 0) != notOdd: clearCodeList.append(element)
    clearCode = "".join(clearCodeList)

    return clearCode

def init(code):
    opened = []
    blocksOfCode = {}
    portals = {}
    for i, char in enumerate(code):
        if char == "[":
            opened.append(i)
        if char == "]":
            if not opened:
                print(f"Cannot find operator '[' for operator ']' at index {i + 1}")
                sys.exit()
            blocksOfCode[i] = opened[-1]
            startIndex = opened.pop()
            blocksOfCode[startIndex] = i
        if char == "G": 
            if code[i + 1] in portals: 
                print(f"Can't create more than one output from goto\nGoto name '{code[i + 1]}' on index {i + 1}")
                sys.exit()
            portals[code[i + 1]] = i + 1

    if opened:
        print(f"Operator '[' on index {opened[0] + 1} opened, but not closed.")
        sys.exit()

    return blocksOfCode, portals
def getblocks(instructions):
    blocks = []
    currentblock = []
    for i in instructions:
        if "label" in i:
            if currentblock:
                blocks.append(currentblock)
            currentblock = [i]
        else:
            currentblock.append(i)
            if i["op"] in ["jmp", "br", "ret"]:
                blocks.append(currentblock)
                currentblock = []
    if currentblock != []:
        blocks.append(currentblock)
    return blocks

import json
import sys
import os
import basicblock

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


# Delete an instruction if it defines a variable that is never used anywhere in the function regardless of control flow
def globaldce(function):
    deleted = False
    # identify all variables ever used globally
    used = []
    for instr in function["instrs"]:
        if "args" in instr:
            used += instr["args"]

    # remove pure assignments that assign to something never used globally
    newinstrs = []
    for instr in function["instrs"]:
        if "dest" in instr and instr["dest"] not in used:
            deleted = True
        else:
            newinstrs.append(instr)
    function["instrs"] = newinstrs

    # whether we made changes
    return deleted

# Delete an instruction if it is later overwritten without being used in the same basic block
# Iterate backwards! :O
def localdce(function):
    deleted = False
    blocks = basicblock.getblocks(function["instrs"])
    newblocks = []
    for block in blocks:
        candidates = set()
        newinstrs = []
        for instr in block[::-1]:
            # iterate through blocks backwards
            if "dest" in instr:
                if instr["dest"] in candidates:
                    # this definition is dead because it is overwritten
                    deleted = True
                    continue
                else:
                    # variable is used later on
                    # but this initialization is currently unused
                    candidates.add(instr["dest"])
            if "args" in instr:
                for arg in instr["args"]:
                    candidates.discard(arg)  # no error for missing elements

            # if we made it here, the instruction should stay
            # remember we're going backwards!
            newinstrs.insert(0, instr)
        newblocks.append(newinstrs)

    function["instrs"] = []
    for block in newblocks:
        function["instrs"] += block
    return deleted


def main():
    bril_program = json.load(sys.stdin)

    for function in bril_program.get("functions", []):
        deleted = True
        while deleted:
            deleted = False
            deleted |= globaldce(function)
            deleted |= localdce(function)

    print(json.dumps(bril_program))


if __name__ == "__main__":
    main()

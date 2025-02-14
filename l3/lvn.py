import json
import sys
import os
import basicblock

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

tablecount = 0


def freshvalue():
    global tablecount
    tablecount += 1
    return tablecount


def getvalue(table, num):
    for v in table.values():
        (n, canon) = v
        if n == num:
            return canon


def lvn(function):
    blocks = basicblock.getblocks(function["instrs"])
    newblocks = []
    for block in blocks:
        newinstrs = []
        table = {}
        cloud = {}  # mapping from variable names to current value numbers
        for instr in block:
            value = None
            # value = (instr["op"], instr["args"])
            if not "op" in instr or instr["op"] == "call":
                continue
            op = instr["op"]
            if op == "const":
                value = (
                    op,
                    tuple([str(instr["value"])]),
                )  # prevent python from treating boolean equal to 0/1
                # print(value)
            elif "args" in instr:
                for a in instr["args"]:
                    if not a in cloud:
                        num = freshvalue()
                        cloud[a] = num  # inputs to basic block
                        table[("inherit", num)] = (
                            num,
                            a,
                        )  # special fake op code for input variables
                mapped = [cloud[arg] for arg in instr["args"]]
                value = (op, tuple(mapped))
            # print(value)

            if value in table:
                num, var = table[value]
                instr.update(
                    {
                        "op": "id",
                        "args": [var],
                    }
                )
            else:
                num = freshvalue()
                # instr["dest"] = newname()
                if "dest" in instr:
                    dest = instr["dest"]
                    table[value] = (num, dest)

                if "args" in instr:
                    # print(instr["args"])
                    instr["args"] = [getvalue(table, cloud[a]) for a in instr["args"]]

            if "dest" in instr:
                cloud[instr["dest"]] = num

        # print(table)


def main():
    bril_program = json.load(sys.stdin)

    for function in bril_program.get("functions", []):
        lvn(function)

    print(json.dumps(bril_program))


if __name__ == "__main__":
    main()

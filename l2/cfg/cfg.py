import json
import argparse


def getblocks(instructions):
    blocks = []
    currentblock = []
    for i in instructions:
        if 'label' in i:
            if currentblock:
                blocks.append(currentblock)
            currentblock = [i]
        else:
            currentblock.append(i)
            if i['op'] in ['jmp', 'br', 'ret']:
                blocks.append(currentblock)
                currentblock = []
    if currentblock != []:
        blocks.append(currentblock)
    return blocks


def labeledblocks(blocks):
    map = {}
    for b in blocks:
        if 'label' in b[0]:
            map[b[0]['label']] = b[1:]
        else:
            map[f"__{len(map)}"] = b
    return map


def cfg(labeledblocks):
    graph = {}
    prev_block = None

    for name in list(labeledblocks.keys()):
        block = labeledblocks[name]
        graph[name] = []

        # fall through case
        if prev_block:
            graph[prev_block].append(name)
            prev_block = None

        # some blocks might only be labels
        if block:
            last = block[-1]

            if last['op'] in ['jmp', 'br']:
                graph[name] = last['labels']
            elif last['op'] == 'ret':
                graph[name] = []
            else:
                prev_block = name
        else:
            prev_block = name

    return graph


def main():
    parser = argparse.ArgumentParser(description="Create a CFG for a Bril program.")
    parser.add_argument("bril", help="Bril JSON file")
    args = parser.parse_args()

    with open(args.bril, "r") as f:
        bril_program = json.load(f)

    for function in bril_program.get("functions", []):
        func_name = function["name"]
        print(func_name + ":")
        labeled_blocks = labeledblocks(getblocks(function["instrs"]))
        graph = cfg(labeled_blocks)
        print(graph)


if __name__ == "__main__":
    main()

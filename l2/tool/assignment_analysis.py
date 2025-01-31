import json
import argparse

def count_variable_assignments(function):
    assignment_counts = {}
    for instr in function["instrs"]:
        if "dest" in instr:
            var_name = instr["dest"]
            assignment_counts[var_name] = assignment_counts.get(var_name, 0) + 1
    return assignment_counts

def main():
    parser = argparse.ArgumentParser(description="Analyze Bril program for variable assignment counts.")
    parser.add_argument("bril", help="Bril file")
    args = parser.parse_args()
    
    with open(args.bril, "r") as f:
        bril_program = json.load(f)
    
    for function in bril_program.get("functions", []):
        func_name = function["name"]
        assignment_counts = count_variable_assignments(function)
        print(func_name+":")
        for var, count in sorted(assignment_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {var}: {count}")

if __name__ == "__main__":
    main()

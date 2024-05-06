#!/usr/bin/env python3

import json

DATABASE_JSON = "results.json"
OUTPUTS = [
    # -> binary no / ish / yes ->
    "SSA",  # tagging = no
    "ETT",  # tagging = ish
    "ETT",  # tagging = yes
]


def predict(args):
    # 0 = no, 1 = ish, 2 = yes
    # "" outputs T, "U" outputs S, so the default must be "ish"
    binary = 1
    tagging = 1
    for arg in args:
        if arg == "b":
            binary = 2
        elif arg == "t":
            binary = 0
        elif arg == "T":
            tagging = 2
            # Hypothesis 1: T resets binary-ness to "ish"
            binary = 1
        elif arg == "U":
            # Hypothesis 2: U resets binary-ness if and only if we're coming from tagging==2
            if tagging == 2:
                binary = 1
            tagging = 0
        else:
            assert False, args
    return OUTPUTS[tagging][binary]


def run():
    with open(DATABASE_JSON, "r") as fp:
        data = json.load(fp)
    success = 0
    fail = 0
    for args, actual_result in data.items():
        expected_result = predict(args)
        if expected_result == actual_result:
            success += 1
        else:
            fail += 1
            print(f"{args}: predicted {expected_result}, should be {actual_result}")
    print(f"{success + fail} tests: {success} correct, {fail} wrong")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3

import subprocess

FLAGS = [
    ("--binary", "b"),
    ("--text", "t"),
    ("--tag", "T"),
    ("--untagged", "U"),
]

CKSUM_PATH = "/scratch/gnu-coreutils/coreutils-git/src/cksum"
MSG_TEXT_UNTAGGED = f"{CKSUM_PATH}: --text mode is only supported with --untagged\nTry '{CKSUM_PATH} --help' for more information.\n"

EXPECTED = {
    (0, "d41d8cd98f00b204e9800998ecf8427e  /dev/null\n", ""): "S",  # Space
    (0, "d41d8cd98f00b204e9800998ecf8427e */dev/null\n", ""): "A",  # Asterisk
    (0, "MD5 (/dev/null) = d41d8cd98f00b204e9800998ecf8427e\n", ""): "T",  # Tagged
    (1, "", MSG_TEXT_UNTAGGED): "E",  # Error
}

MAX_NUM_ARGS = 5  # 1024 + 256 + 64 + 16 + 4 + 1 combinations
# MAX_NUM_ARGS = 4  # 256 + 64 + 16 + 4 + 1 combinations
# MAX_NUM_ARGS = 3  # 64 + 16 + 4 + 1 combinations
# MAX_NUM_ARGS = 2  # 16 + 4 + 1 combinations


def generate_indices(num_args):
    assert num_args >= 0
    if num_args == 0:
        yield []
        return
    for indices in generate_indices(num_args - 1):
        for appended in range(len(FLAGS)):
            indices.append(appended)
            yield indices
            indices.pop()


def run_indices(indices, fp):
    args = [FLAGS[i][0] for i in indices]
    args_shortdesc = "".join(FLAGS[i][1] for i in indices)
    result = subprocess.run(
        [CKSUM_PATH, "--algo=md5", *args, "/dev/null"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
    )
    result_tuple = (result.returncode, result.stdout, result.stderr)
    behavior_name = EXPECTED.get(result_tuple, None)
    if behavior_name is None:
        print(f"Unknown behavior for '{args_shortdesc}'?! -> {result_tuple}")
        behavior_name = "?"
    pre_comma = "" if indices == [] else ","
    fp.write(f"{pre_comma}\"{args_shortdesc}\": \"{behavior_name}\"\n")


def try_num_args(num_args, fp):
    print(f"Trying up to {num_args} args ({4 ** num_args} combinations) ...")
    for indices in generate_indices(num_args):
        run_indices(indices, fp)


def run():
    with open("results.json", "w") as fp:
        fp.write("{\n")
        for num_args in range(MAX_NUM_ARGS + 1):
            try_num_args(num_args, fp)
        fp.write("}\n")


if __name__ == "__main__":
    run()

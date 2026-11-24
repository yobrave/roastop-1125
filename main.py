# r19 operator-roast emitter (bytes-first layout)
import json
import os
import sys

BOUND = 140
NAME = "roastop-1125"
MARK = "r19 warm roast"


def slurp():
    root = os.path.split(os.path.abspath(__file__))[0]
    blob = open(os.path.join(root, "entry.txt"), "rb").read()
    text = blob.decode("utf-8").replace("\r", "").strip()
    return text


def verify(text):
    problems = []
    if len(text) == 0:
        problems.append("no content")
    if len(text) > BOUND:
        problems.append("over bound")
    if len(text.split()) == 0:
        problems.append("no words")
    return problems


def put_out(text):
    place = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(place, exist_ok=True)
    full = os.path.join(place, "entry.txt")
    with open(full, "wb") as handle:
        handle.write(text.encode("utf-8"))
    seen = open(full, "rb").read().decode("utf-8")
    if seen != text:
        problems = ["echo differs"]
        raise RuntimeError(problems)
    return full


def go():
    text = slurp()
    bad = verify(text)
    if bad:
        print(json.dumps({"name": NAME, "bad": bad}))
        return 3
    full = put_out(text)
    print(json.dumps({"name": NAME, "mark": MARK, "full": full,
                      "bound": BOUND, "len": len(text), "verdict": "clean"}))
    return 0


if __name__ == "__main__":
    sys.exit(go())

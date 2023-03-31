import json
import sys


def add_dicts(d1, d2):
    def sum(v1, v2):
        if v2 is None:
            return v1
        try:
            return v1 + v2
        except TypeError:
            return add_dicts(v1, v2)

    result = d2.copy()
    result.update({k: sum(v, d2.get(k)) for k, v in d1.items()})
    return result

d = []
result = {}
for f in sys.argv[1:]:
    result = add_dicts(result, json.load(open(f, 'r')))

json.dump(result, open("final_stats.json", 'w'))
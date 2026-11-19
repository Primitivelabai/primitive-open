#!/usr/bin/env python3
"""Public synthetic CPU fixture verifier; no proprietary implementation included."""
import argparse
import json

CASES = [
    (1000, 1, 10, 1000, 86898),
    (1000, 100, 1, 1000, 105000),
    (10000, 120, 1, 100, 3500),
    (10000, 120, 100, 100, 9177),
    (10000, 120, 100, 10000, 926800),
    (30000, 120, 1000, 30000, 2676030),
    (10000, 2, 1000, 10000, 907886),
]
MASK = (1 << 32) - 1


def sequence(seed):
    while True:
        seed ^= (seed << 13) & MASK
        seed ^= seed >> 17
        seed ^= (seed << 5) & MASK
        seed &= MASK
        yield seed


def verify():
    rng = sequence(20261118)
    output = []
    for n, steps, groups, reads, expected in CASES:
        values = [next(rng) % 27 for _ in range(n)]
        controls = [[(next(rng) % 27, next(rng) % 27) for _ in range(groups)] for _ in range(steps)]
        for row in controls:
            for i in range(n):
                a, b = row[i % groups]
                values[i] = (a * values[i] + b) % 27
        checksum = sum(values[:reads]) * 7
        output.append(dict(n=n, steps=steps, groups=groups, reads=reads,
                           expected_checksum=expected, observed_checksum=checksum,
                           exact=checksum == expected))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = verify()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for i, row in enumerate(results, 1):
            print(f"case {i}: {row['observed_checksum']} / {row['expected_checksum']} "
                  f"{'PASS' if row['exact'] else 'FAIL'}")
    raise SystemExit(0 if all(row["exact"] for row in results) else 1)

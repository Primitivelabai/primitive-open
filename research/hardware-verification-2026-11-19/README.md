# Primitive AI hardware verification: synthetic CPU fixture

This small public fixture gives a prospective Perth hardware collaborator something executable before agreeing to a workstation loan. It contains synthetic inputs, a conventional scalar reference replay and seven expected checksums. It does **not** contain Primitive AI's optimized research implementation or unpublished optical-search code.

## Run

Python 3.9 or newer, standard library only:

```sh
python3 verify.py
python3 verify.py --json
```

The program exits nonzero if any checksum differs. Expected result: seven PASS lines. The fixtures apply per-group affine updates over integers modulo 27, using a fixed xorshift32 input stream. The generator state continues across cases. All requested outputs contribute to each checksum; a checksum match is a useful check but does not prove element-by-element equality.

## Evidence boundary

The seven expected checksums came from the C11 CPU benchmark in Primitive AI's private source handoff. This public script independently calculates the scalar reference on the same synthetic fixture. It verifies the published expected checksums on a new host; it does **not** reproduce the optimized timing ratios, compare every element with the C output, establish independent third-party replication, measure GPU performance, or validate the separate 608-case optical result. Those tasks require pinned implementations, raw per-repeat outputs, hardware and environment metadata, and a separate review.

The internal optical report describes a synthetic finite-grid search where 608/608 selected grid winners matched exhaustive NumPy and a warm five-run batch median was 119.95 ms versus 1,569.23 ms for an earlier compiled method. Cold compilation was excluded. That figure is background context, **not a result verified by this repository**.

## Independent hardware run protocol

1. Record GPU/CPU model, system RAM, OS, Python/CUDA/driver versions, power settings and source commit.
2. Verify the provided source hashes before running any separately supplied benchmark executable.
3. Run this public reference script. For the performance comparison, run named conventional and candidate implementations on identical generated inputs, compare complete requested outputs with an independently written scalar reference, and retain failures.
4. Record at least seven raw repetitions per case, cold-start and warm timings, device-only and transfer-inclusive timings, compilation/setup cost, memory footprint and exact commands.
5. Publish the raw log with the shop's agreed credit and no promised positive conclusion. Private code disclosure, if any, requires a separate agreement.

This is a verification entry point and protocol, not a public claim of GPU speedup or a general AI benchmark.

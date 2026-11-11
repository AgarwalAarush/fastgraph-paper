"""Validate Table 2 against the paired aggregate CSV shipped with this draft."""
from collections import defaultdict
import csv
import math
from pathlib import Path
import statistics


packet = Path(__file__).resolve().parent
with open(packet / "timing-repeatability.csv", newline="") as handle:
    repeats = list(csv.DictReader(handle))
assert repeats and all(int(row["measured_repetitions"]) == 3 for row in repeats)
print(f"All {len(repeats)} timing configurations contain three measured repetitions.")
with open(packet / "paired-exact-comparisons.csv", newline="") as handle:
    rows = list(csv.DictReader(handle))
expected = [
    ("anisotropic_0.99", 8, "0.300", "22.21", "20.89", "23.61"),
    ("anisotropic_0.90", 8, "1.383", "4.82", "4.63", "5.02"),
    ("gaussian", 8, "7.151", "0.93", "0.92", "0.93"),
    ("gaussian", 10, "12.389", "0.53", "0.53", "0.54"),
]
for distribution, dim, seconds, speedup, low, high in expected:
    grouped = defaultdict(list)
    for row in rows:
        if (row["source"], row["distribution"], int(row["dim"]), int(row["points"]),
            int(row["k"]), int(row["events"]), row["transform"]) == (
                "synthetic", distribution, dim, 1_000_000, 40, 1, "raw"):
            grouped[row["seed"], row["input_hash"], row["hardware_hash"]].append(row)
    assert len(grouped) == 3 and len({key[0] for key in grouped}) == 3
    times = [statistics.median(float(r["pca_ms"]) for r in group) / 1000 for group in grouped.values()]
    ratios = [statistics.median(float(r["cuvs_bf_over_pca"]) for r in group) for group in grouped.values()]
    logs = list(map(math.log, ratios))
    center = statistics.mean(logs)
    half = 4.302652730 * statistics.stdev(logs) / math.sqrt(3)
    actual = (f"{statistics.median(times):.3f}", f"{math.exp(center):.2f}",
              f"{math.exp(center-half):.2f}", f"{math.exp(center+half):.2f}")
    assert actual == (seconds, speedup, low, high), (distribution, dim, actual)
    print(distribution, dim, "three independent seeds; table agrees:", *actual)

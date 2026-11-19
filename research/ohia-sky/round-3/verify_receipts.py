"""Verify the published OHIA Sky campaign receipts with Python's standard library."""

import csv
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    public = ROOT if (ROOT / 'public_receipts.json').is_file() else ROOT / 'run'
    roster = ROOT / ('target_roster.csv' if public == ROOT else 'data/target_roster.csv')
    data = json.loads((public / 'public_receipts.json').read_text())
    with roster.open(newline='') as source:
        targets = list(csv.DictReader(source))
    assert sha256(roster.read_bytes()).hexdigest() == data['roster_sha256']
    assert len({row['kepid'] for row in targets}) == data['selected'] == 116
    assert data['eligible'] == sum(data['eligible_cohorts'].values())
    assert data['prior_known'] + len(data['recovered_known_planets']) == data['combined_known']
    assert len(data['recovered_known_planets']) == data['dense'] + data['pool'] - data['dense_pool_intersection']
    assert data['routed'] == data['dense'] - len(data['dense_missed_by_route']) + len(data['route_extra_over_dense'])
    print('PASS roster and disjoint recovery counts')
    with (public / 'rank_audit.csv').open(newline='') as handle:
        ranks = list(csv.DictReader(handle))
    assert len(ranks) == data['rank']['candidate_windows']
    assert sum(Fraction(row['integer_direct']) == Fraction(row['integer_index']) for row in ranks) == data['rank']['integer_exact']
    assert sum(float(row['float_reference']) == float(row['float_index']) for row in ranks) == data['rank']['float_exact']
    assert sum(float(row['float_reference']) != float(Fraction(row['integer_index'])) for row in ranks) == data['rank']['quantization_changed_rank']
    print('PASS integer and floating-point witness rank comparisons')
    assert sum(r['trials'] for r in data['injections']) == 192
    assert all(r['trials'] == r['correct'] + r['abstained'] + r['wrong'] for r in data['injections'])
    assert not any(r['wrong'] for r in data['injections'])
    print('PASS 192 injection classifications and abstentions')
    pixels = data['pixels']['results']
    assert {r['quarter'] for r in pixels} == {11, 12, 15, 16, 17}
    assert all(r['peak_to_neighbor_px'] < r['peak_to_target_px'] and r['neighbor_favored_widths'] == 4 for r in pixels)
    print('PASS five held-out pixel localizations')


if __name__ == '__main__':
    main()

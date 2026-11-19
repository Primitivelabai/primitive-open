"""Verify the public OHIA Sky evidence receipt with Python's standard library."""

from collections import Counter
from math import comb, isclose
from pathlib import Path
import json


def fisher_one_sided(a, b, n_inside, n_outside):
    total = n_inside + n_outside
    signal = a + b
    denominator = comb(total, n_inside)
    return sum(comb(signal, x) * comb(total - signal, n_inside - x)
               for x in range(a, min(n_inside, signal) + 1) if n_inside - x <= total - signal) / denominator


def check(condition, description):
    if not condition:
        raise SystemExit(f'FAIL {description}')
    print(f'PASS {description}')


def main():
    content = json.loads(Path(__file__).with_name('evidence.json').read_text())
    planet_rows = content['planet_signals']
    check(len({(row['kepid'], row['reference']) for row in planet_rows}) == 56,
          '56 distinct catalogue-matched planets')
    count = Counter(row['kepid'] for row in planet_rows)
    check(len(count) == 41 and sum(value >= 2 for value in count.values()) == 12,
          '41 hosts and 12 multi-planet recoveries')
    check(sum(row['search_pass'] > 1 for row in planet_rows) == 13,
          '13 planet recoveries after masking an earlier signal')
    memberships = content['stellar_membership_checks']
    check(sum(row['catalogue_id_matches'] for row in memberships) == 775
          and sum(row['inside_gate'] for row in memberships) == 790
          and sum(row['catalogue_heldout_id_matches'] for row in memberships) == 392
          and sum(row['inside_heldout_gate'] for row in memberships) == 398, 'stellar membership agreement')
    image = content['image_metrics']['test_ohia']
    check(isclose(image['true_calls'] / (image['true_calls'] + image['false_calls']), image['precision'])
          and isclose(image['true_calls'] / image['positive'], image['recall']), 'held-out image precision and recall')
    groups = content['galaxy_windows']
    check(len(groups) == 41 and sum(bool(row['abell_match'] or row['tempel_match'] or row['tempel_dr8_match'])
                                    for row in groups) == 40, '41 Sloan windows and 40 catalogue matches')
    statistic = content['desi_checks']
    for row in statistic:
        a, b = row['desi_aperture_window'], row['desi_control_window']
        n_inside, n_outside = row['desi_aperture_parent'], row['desi_control_parent']
        p = fisher_one_sided(a, b, n_inside, n_outside) if n_inside and n_outside else 1.0
        check(isclose(p, row['desi_exact_local_p'], rel_tol=1e-11, abs_tol=1e-300)
              and isclose(min(1.0, len(statistic) * p), row['desi_bonferroni_p'], rel_tol=1e-11),
              f'DESI contingency counts and correction for {row["id"]}')


if __name__ == '__main__':
    main()

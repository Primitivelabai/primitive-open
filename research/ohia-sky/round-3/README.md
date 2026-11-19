# OHIA Sky round 3

**Independent Kepler checks and Lean proofs · 19 November 2026 (Perth)**

The pooled search recovered **the same 22 catalogued planets as the dense search** on 103 eligible, previously unsearched Kepler targets. The measured search stage used **8.39× less summed per-target time**. The ledger now contains **90 previously catalogued planets**. This campaign confirmed zero new planets.

## Lean proofs

[OhioSky.lean](OhioSky.lean) contains eight theorems checked in Lean 4.19.0 with warnings treated as errors and no `sorry` admissions. The theorems cover interval sums by prefix subtraction, wrapping on a circular list, preservation of weighted rank votes, folding a signal at any integer multiple of its period, and preservation of that alias under linear aperture contamination. A constructed counterexample shows that a once-per-long-cycle dip and a three-times-per-cycle wave agree at the main anchors. An internal crossing separates them. A final theorem checks the less-than-two-second difference from an exact 3:1 ratio using the measured periods rounded to nanodays.

The rank theorems start with ordered integer samples and specified window endpoints. The numerical comparisons audit the Python code, the endpoint masks and rounding. The astronomical attribution rests on the observations.

```sh
lean -DwarningAsError=true OhioSky.lean
python3 verify_receipts.py
```

## Campaign results

| Check | Outcome |
| --- | --- |
| Fresh search | 116 disjoint target IDs, 558 usable archive products out of 580 requested, 103 eligible targets. Q5–Q7 generated proposals, Q8–Q9 tested 389 frozen candidate clocks. |
| Dense and pooled search | Both recovered the same 22 known planets. Summed per-target search times were 235.22 s dense and 28.03 s pooled. This boundary includes proposal refinement and early checks, and excludes downloads and later verification. |
| Selective fallback | The previously proposed rule to deepen only catalogued multiple-planet hosts was evaluated on the fresh roster. A replay on the measured timings deepened 16 targets, retained all 22 recoveries and used 94.83 s. The pooled arm already recovered all 22 in this cohort. |
| Phase index | Direct integer masks and prefix extraction yielded identical counts and sums for all 389 candidates. All ranks agreed with the original float matrix, including after rounding to 1 nanoday and 0.01 ppm. This agreement is empirical for the checked inputs. |
| Internal-phase witness | Injected once-per-cycle and three-times-per-cycle dips at known phases into later cadence data from 24 stars. The witness classified 182 of 192 correctly, abstained on 10 and made zero errors. At 50 ppm it got 40/48 and at 100 ppm it got 46/48. At 250 and 500 ppm it got 48/48 each. This test supplies the trial clock and uses idealized boxes. |
| Independent pixel check | The five target-pixel quarter products omitted from the round-two pixel comparison were Q11, Q12, Q15, Q16 and Q17. The difference-image peak from a blind spatial grid was closer to the bright neighbor in 5/5 cases, within 0.25–0.80 pixel. The two-source comparison favored that neighbor across all 20 quarter-by-width combinations. |

## The two false alarms

**Round-two neighbor.** The five new pixel products support the attribution of the apparent 1.114598-day signal on KIC 11607008 to KIC 11607017. The separate stellar light curve in round two fit a 0.371540-day pulsation. Three periods are within 1.97 seconds of the apparent transit clock. Subtracting the stellar modes fit on Q5–Q9 removed the apparent dip on later and earlier photometry. The five new results extend the earlier 11 pixel localizations. See [Gebruers et al.](https://doi.org/10.1051/0004-6361/202140466) and the [MAST Kepler pixel-data guide](https://spacetelescope.github.io/mast_notebooks/notebooks/Kepler/verifying_the_location_of_a_signal/verifying_the_location_of_a_signal.html).

**Fresh lead.** KIC 7750128 produced a 1.810645-day signal, near half the 3.64-day stellar rotation period listed by two independent catalogue studies of the Kepler observations. On the 13 quarters outside Q5–Q9, the detrended cotrended series had an apparent dip of 840 ppm and an opposite-phase brightening of 827 ppm. A sinusoid fitted on Q5–Q9 reduced the held-out dip to 34 ppm (event SNR 1.32). In the separate aperture product the corresponding 832 ppm dip fell to 27 ppm (event SNR 1.01). These checks support stellar variability as the explanation. They leave the specific surface mechanism open. [McQuillan et al. catalogue](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FApJS%2F211%2F24%2Ftable1&KIC=7750128) · [Santos et al. catalogue](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FApJS%2F255%2F17%2Ftable1&KIC=7750128)

A post-hoc veto for strong opposite-phase brightening removed both rounds' unmatched alerts and retained all 39 and 22 catalogued recoveries in the respective rounds. It still admitted four round-three hosts from the labelled false-positive cohort. The result is a bounded check on these archives. The public [receipts](public_receipts.json) include the veto thresholds, aperture fits, frozen target list and rank audit.

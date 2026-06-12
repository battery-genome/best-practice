---
id: method:ici
title: Intermittent Current Interruption (ICI)
summary: Resistance and diffusion characterization from brief, regular current interruptions during constant-current cycling — quasi-continuous R and k values, and solid-state diffusion coefficients in a fraction of the time GITT requires.
version: 0.1.0
status: published
test_kinds: [ici]
authors:
  - name: Simon Clark
    orcid: null
    affiliation: SINTEF
sources:
  - role: primary
    title: Rapid determination of solid-state diffusion coefficients in Li-based batteries via intermittent current interruption method
    authors: Yu-Chuan Chien, Haidong Liu, Ashok S. Menon, William R. Brant, Daniel Brandell, Matthew J. Lacey
    year: 2023
    venue: Nature Communications 14, 2289
    doi: 10.1038/s41467-023-37989-6
    license: CC-BY-4.0
    note: Theory and equations, recommended experimental parameters, validation against GITT and EIS, and the stated assumptions and limitations.
  - role: primary
    title: "ICI — Intermittent Current Interruption (project page)"
    authors: Matthew J. Lacey
    url: https://lacey.se/projects/ici
    accessed: 2026-06-12
    note: Method overview and development history (ICI 1.0-4.0), practical parameter choices, instrument compatibility, and demonstrated chemistries.
related_practices: []
related_protocols: []
created_at: 2026-06-12
updated_at: 2026-06-12
---

# Intermittent Current Interruption (ICI)

## Overview

ICI characterizes a cell's internal resistance and mass-transport behavior by
inserting brief, regular current interruptions into an otherwise ordinary
constant-current charge/discharge cycle, and analyzing the voltage response
during each pause. Developed by Matthew J. Lacey and co-workers from 2015
onward, it yields two parameters as quasi-continuous functions of state of
charge — an internal resistance **R** and a diffusion resistance coefficient
**k** — and, with knowledge of the open-circuit potential slope, solid-state
diffusion coefficients comparable to GITT in well under a fifth of the
experimental time.

Choose ICI when you want resistance and diffusion information *throughout*
cycling rather than at a few dedicated checkpoints: degradation tracking over
hundreds of cycles, operando experiments where long GITT relaxations are
impossible, or routine characterization without an impedance analyzer. It has
been demonstrated on lithium-ion chemistries (LCO, NMC, LFP, LNMO),
lithium-sulfur, sodium-ion, and nickel-metal hydride cells.

## Principle

When the current **I** is interrupted, the voltage relaxes in a
characteristic pattern: an immediate step from ohmic and fast interfacial
(charge-transfer) contributions, followed by a slower change governed by
diffusion. Under diffusion control the voltage is linear in the square root
of the time **Δt** since the interruption:

```
ΔE(Δt) = −I·R − I·k·√Δt
```

A linear regression of potential against √Δt for each pause therefore gives
both parameters at once:

- **R** (Ω, or Ω·cm² area-normalized) from the intercept — the resistive
  contribution following Ohm's law;
- **k** (Ω·s⁻¹ᐟ², or Ω·cm²·s⁻¹ᐟ²) from the slope — the mass-transport
  contribution to the potential change, closely related to the Warburg
  coefficient measured by EIS.

Both parameters are directly connected to physical phenomena and are
independent of the applied current and the interruption timing, which is what
makes values comparable across experiments.

Combining k with the slope of the (pseudo-)open-circuit potential curve gives
a solid-state diffusion coefficient, in direct analogy to GITT. As derived by
Chien et al. (2023):

```
D = (4/π) · ( (V/A) · (ΔE_OC/Δt_I) / (dE/d√t) )²
```

where V is the volume of active material, A its electrochemically active
surface area, ΔE_OC/Δt_I the rate of change of the iR-corrected potential
during the current step, and dE/d√t the fitted diffusion slope.

## Procedure

ICI is a small modification of a test you are already running; it needs no
special hardware beyond a cycler with adequate voltage resolution and
sampling rate.

1. Cycle the cell galvanostatically at a low rate — **C/10 to C/20** is
   typical; C/10 was used in the validation study to keep electrolyte
   concentration gradients small.
2. Insert a **complete current interruption of 1–10 s** at regular intervals
   of **every 5–15 minutes** (a common choice is 5 s every 5 min; the
   validation study used 10 s every ~15 min). The rest of the schedule is
   unchanged.
3. Sample voltage at **≥ 10 Hz during the interruptions** (0.1 s resolution
   in the validation study). Between interruptions, normal logging rates
   suffice.
4. Record time, voltage, and current continuously, including the pause
   periods. If electrode-resolved values are needed, use a three-electrode
   cell; otherwise any cell format works.

The added test time is a few percent of the total — the practical cost of
ICI over plain cycling is negligible.

## Analysis

For each interruption:

1. Select the diffusion-controlled fitting window, typically **1–5 s after
   the interruption begins** (the first instants contain the ohmic step and
   double-layer response; too late and the semi-infinite assumption fails).
2. Fit potential against √Δt by linear regression: intercept → R,
   slope → k (divide by −I as per the equation above).
3. Plot R and k against capacity or state of charge — one pair of values per
   interruption gives quasi-continuous curves for every cycle, so resistance
   and diffusion evolution can be tracked across ageing.
4. For diffusion coefficients, combine k with the local pseudo-OCP slope as
   in the equation above. Validation against GITT on NMC811 showed agreement
   with roughly 26% relative standard deviation — small compared to the two
   orders of magnitude over which literature GITT values for the same
   material scatter.

**Pitfalls to respect:**

- **Semi-infinite diffusion assumption.** The √t analysis is valid only while
  the diffusion length is small compared to the particle size
  (Δt ≪ L²/D). Keep the fitting window short.
- **Charge-transfer interference.** Where charge-transfer resistance is large
  (e.g. NMC811 below ~3.7 V), the diffusion signature shifts outside the
  fitting window and ICI and GITT disagree substantially. Treat low-SOC
  values with caution.
- **Single-phase assumption.** Inherited from GITT theory; the diffusion
  interpretation is invalid during phase transitions (the R and k parameters
  themselves remain well-defined descriptors).
- **Geometry uncertainty.** D scales with (V/A)²; uncertainty in the
  electrochemically active surface area propagates quadratically.
- The pseudo-OCP approximation uses iR-corrected potential under load rather
  than a true rest measurement; its validity degrades as charge-transfer
  resistance grows.

## Variants and related methods

- **vs. GITT:** both rest on the same diffusion theory, but GITT requires
  long relaxations to equilibrium after each titration step; ICI replaces
  them with seconds-long interruptions and needs less than 15% of the
  experimental time, at the price of the pseudo-OCP approximation above.
- **vs. EIS:** R and k capture similar information to the high-frequency
  resistance and Warburg response without a frequency response analyzer or
  equivalent-circuit fitting, and while the cell is cycling normally. EIS
  remains better at separating individual processes by their time constants.
- The method has evolved through several formulations — from the original
  lithium-sulfur application (2015) through generalized resistance analysis
  to the diffusion-coefficient connection (2023). The ICI project page
  tracks the full publication history.

## References

- Y.-C. Chien, H. Liu, A. S. Menon, W. R. Brant, D. Brandell, M. J. Lacey,
  *Rapid determination of solid-state diffusion coefficients in Li-based
  batteries via intermittent current interruption method*, Nature
  Communications 14, 2289 (2023). https://doi.org/10.1038/s41467-023-37989-6
  (CC-BY 4.0)
- M. J. Lacey, *ICI — Intermittent Current Interruption*, project page with
  full publication history. https://lacey.se/projects/ici

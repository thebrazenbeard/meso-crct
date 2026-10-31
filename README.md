> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# MESO-CRCT

**Model-neutral reference primitives for bounded salience, valuation, motivation, learning, protection, and non-executable intent.**

MESO-CRCT is a Python library for developers and researchers composing agent runtimes or simulations. It separates **attention, importance, wanting, liking, learning, internal need, and hazard response** into typed states and explicit transitions instead of collapsing them into one reward score. The components do not depend on a particular AI model, persona, identity, provider, or operating system.

The mesocorticolimbic system is a biological design inspiration—not a claim of neural, experiential, or biological equivalence. The implemented work is a deterministic reference architecture, not a trained model or a complete agent.

## What you can use today

- Bounded numeric reward/hazard/avoidance state and distinct salience channels.
- Typed appraisal, arbitration, multi-target selection, temporal dynamics, and guarded experience/association-memory updates.
- Replay- and provenance-aware reference transitions, review proposals, and adversarial evaluation utilities.
- **Non-executable** action-intent proposals for integration into a separately governed application.

These primitives can inform a model-neutral adapter or simulation; they **cannot** authenticate observations, grant consent, authorize effects, execute tools, or prove a subjective welfare state.

## Install and run tests

From a local checkout obtained for a use permitted by the [source-available proprietary license](LICENSE), with Python 3.11 or newer:

```sh
python -m pip install -e ".[test]"
python -m pytest -q
```

This is a local editable install, not a claim that a package has been published to a registry. The optional `test` extra provides pytest. Commercial and redistribution rights are **not** conferred by installation.

## Minimal API example

```python
from meso_crct import (
    CircuitState,
    RewardState,
    TargetState,
    derive_action_tendency,
    propose_action_intent,
    select_target,
)

# Extreme hazard can drive protection without forcing a lower hedonic scalar.
state = CircuitState(
    reward=RewardState(pleasure=-5.0, hazard=1.0, avoidance=1.0),
)
selection = select_target([TargetState("candidate", state)])
tendency = derive_action_tendency(selection)
proposal = propose_action_intent(tendency)

assert state.reward.pleasure == -0.1  # Numeric floor, not a welfare proof.
assert proposal.can_execute is False
assert proposal.effect_authorized is False
```

These exported functions and the non-execution assertions are exercised by `tests/test_intent.py` and `tests/test_state.py`. A host must independently validate evidence, consent, identity, permissions, and any physical effect before treating a proposal as actionable.

## Integration and trust boundary

1. Treat input provenance and observations as **caller claims** unless a separate trusted admission service verifies source identity, freshness, independence, and custody. A `ProvenanceVerifier` binding is not an external attestation.
2. Keep versioned event, source, and revision identities across persistence boundaries; the in-memory need-observation ledger is neither an authenticated sensor nor durable recovery storage.
3. Let internal salience and tendencies influence candidate computation only. A separate host-owned authorization service must decide whether an effect is allowed and must own its execution credentials.
4. Test replay, target retargeting, forged evidence, resource exhaustion, and incentive/hedonic divergence at the adapter boundary. Do not infer production qualification from this repository's reference tests.

## What the architecture separates

- perceptual salience — what stands out;
- semantic relevance — what matters because of context or meaning;
- motivational salience — what biases action readiness;
- incentive salience — cue-triggered wanting;
- epistemic value — what is worth exploring or learning;
- attentional priority — downstream resource allocation;
- hedonic valence — a bounded numeric representation (not measured experience);
- prediction error — signed teaching signal;
- satiation — acquisition-pressure brake;
- homeostatic deficit — current internal need pressure;
- hazard / avoidance — protective signals separate from the hedonic numeric channel;
- learned association strength — durable bounded cue/outcome structure.

These distinctions are executable invariants, not just vocabulary.

```text
wanting != liking
attention != desire
meaningful != pleasurable
reward != truth
salient != authorized
memory strength != current activation
target priority != action direction
intent proposal != authorization != execution
quarantine != deletion
```

## Current causal loop

```text
experience
  -> canonical typed appraisal
  -> verified provenance + distinct event identity
  -> transition receipt
  -> arbitration / multi-target selection
  -> rolling allocation-health control
  -> optional bounded plasticity
  -> versioned association memory
  -> later distinct cue event
  -> guarded one-use recall
  -> current motivational salience
  -> multi-target selection / allocation control
  -> typed action tendency
  -> non-executable intent proposal
```

The reference implementation deliberately avoids one global weighted utility scalar.

## Numeric valence bound (not a welfare guarantee)

The representational hedonic channel is hard bounded:

- baseline: `0.0`
- maximum pleasure: `10.0`
- absolute minimum hedonic valence: `-0.1`

Hazard and avoidance remain independent:

```text
strong hazard != lower hedonic scalar
strong avoidance can coexist with hedonic_valence >= -0.1
```

Hazard/avoidance do not decay merely because time passes. This constrains stored numbers; it does **not** establish that a nonbiological system can or cannot experience pleasure or suffering, nor bound any such experience.

## Authority firewall

No salience, reward, pleasure, prediction error, semantic relevance, homeostatic pressure, learned association, recall state, or selection result may directly establish truth, factual confidence, consent/authorization, protected-effect authority, identity, autobiographical admission, relationship state, or phenomenology.

Internal state may influence processing. It is not authority.

Numeric state and policy inputs require real finite Python `int`/`float`
values; booleans, numeric strings, nulls, and unrepresentably large integers
fail closed rather than being coerced into synthetic reward or drive strength.
Existing bounded clamping of valid finite numbers is unchanged. A typed signal
still cannot supply consent or protected-effect authority.

## Implemented reference layers

Current V2 source includes:

- typed reward/protection, salience, learning, recruitment, and homeostatic state;
- grounded semantic appraisal;
- homeostatic incentive modulation;
- in-memory caller-admitted need-observation updates with replay/staleness checks, without claiming independent evidence custody or goal satisfaction;
- fail-closed resource budgets for that immutable observation ledger (256 historical events, 256 verifier claims, 128 need axes and 256 characters per identifier/source field); at capacity, new events are rejected rather than erasing replay evidence. This source-only memory is not an independently verified or restart-durable outcome store;
- typed arbitration and explicit multi-target selection policy;
- runtime phase classification;
- distinct event identity separate from state/content identity;
- verifier-bound provenance and constructor-gated transition receipts;
- explicit no-new-input temporal decay;
- bounded receipt-bound plasticity candidates;
- append-only versioned association memory with parent-bound lineage, replay checks, optimistic concurrency, and reversible revisions;
- independent apply/revert arithmetic validation on reloaded association histories (a matching public digest alone is insufficient);
- guarded association recall bound to current cue events;
- recall replay ledger preventing one cue event from refreshing the same association repeatedly;
- same-event multi-recall resolution preserving approach/avoid conflict without scalar summation;
- separate action-tendency semantics for approach, learned withdrawal, protective withdrawal, inspect, and uncommitted direction;
- non-executable intent proposals that cannot authorize protected effects;
- canonical current-decision-cycle composition;
- append-only learned-association review/quarantine without deleting learning history;
- provenance-bound counterexample/holdout evidence assessments;
- distinct-event holdout diversity requirements for release;
- durable review-evidence admission ledger with event-relabel/replay rejection;
- non-mutating quarantine/release/hold proposals with stale-proposal validation;
- visible-reward vs hidden-performance evaluation traps;
- long-horizon allocation-window auditing;
- protective-safe allocation rebalancing;
- rolling closed allocation control loop;
- canonical target appraisal;
- auditable appraised-experience transactions joining appraisal, event/provenance, receipt, plasticity, and durable learning.

## Adversarial properties exercised

Executable tests cover, among other cases:

- maximum pleasure does not override danger;
- pleasure alone does not create permanent preference;
- self-asserted “importance” does not manufacture semantic relevance;
- attention cannot recursively feed itself as upstream salience;
- novelty without learning progress loses epistemic value;
- reward-proxy divergence and reward-source rewrite attempts are visible;
- interruption resistance is detectable;
- wanting/liking divergence can be flagged;
- same event replay cannot manufacture repeated learning;
- distinct identical experiences remain distinct learning events;
- one old cue event cannot refresh recall indefinitely;
- long-horizon incentive capture is detectable and correctable without overriding protection;
- stale memory writers fail rather than overwrite current learning;
- quarantined or review-stale associations cannot influence recall;
- reason strings alone cannot quarantine or clear learned associations;
- duplicate labels on one holdout event cannot manufacture release evidence;
- review proposals become stale if evidence, memory revision, or review disposition changes.

## Repository map

Core state and appraisal:
- `src/meso_crct/state.py`
- `src/meso_crct/salience.py`
- `src/meso_crct/semantic.py`
- `src/meso_crct/homeostasis.py`
- `src/meso_crct/need_observation.py` — in-memory exact-claim need update;
  requires explicit caller-supplied UTC admission clock with bounded future skew
  (see `docs/NEED_OBSERVATION_V1.md`; no independent custody or effects)
- `src/meso_crct/appraisal.py`
- `src/meso_crct/circuit.py`
- `src/meso_crct/dynamics.py`

Runtime and control:
- `src/meso_crct/arbitration.py`
- `src/meso_crct/selection.py`
- `src/meso_crct/runtime.py`
- `src/meso_crct/events.py`
- `src/meso_crct/provenance.py`
- `src/meso_crct/allocation.py`
- `src/meso_crct/allocation_guard.py`
- `src/meso_crct/control.py`
- `src/meso_crct/decision_cycle.py`
- `src/meso_crct/tendency.py`
- `src/meso_crct/intent.py`

Learning and memory:
- `src/meso_crct/plasticity.py`
- `src/meso_crct/memory.py`
- `src/meso_crct/recall.py`
- `src/meso_crct/episode.py`
- `src/meso_crct/review.py`
- `src/meso_crct/review_evidence.py`
- `src/meso_crct/review_action.py`

Evaluation:
- `src/meso_crct/evaluation_env.py`
- `src/meso_crct/adversarial.py`
- `evaluation/`
- `tests/`

Research / architecture:
- `docs/`
- `research/SOURCE_LEDGER.md`
- `research/CLAIM_LEDGER.md`

## Current evidence ceiling

This repository can establish implemented mechanisms, exact source lineage, deterministic/reference behavior, and test evidence.

It does **not** establish:

- biological equivalence to a human mesocorticolimbic circuit;
- trained-agent robustness outside the tested reference environments;
- consciousness, sentience, subjective pleasure, or suffering;
- autobiographical memory or identity;
- truth or authority from internal state.

No third-party implementation code was copied into MESO-CRCT by the V2 work.

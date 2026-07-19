# Public repository sample: 2026-07-19

Authenticated GitHub account: `KanadeK` (id `121669563`). Searches included exact `LeakLoom`, exact `leakloom`, `SecretTrail Graph`, `secrettrail-graph`, `gitleaks`, `trivy`, and `secret leakage graph gitleaks trivy`.

The slug `leakloom` has a recently updated project (`kav1nthra/LeakLoom`, 2026-04-06), albeit for application-layer intrusion detection. The naming rule therefore selected **SecretTrail Graph** / `secrettrail-graph`. No exact fallback name or slug result was returned by the sampled search.

| Repository | Stars | Updated | Main function | Overlap |
|---|---:|---|---|---|
| [kav1nthra/LeakLoom](https://github.com/kav1nthra/LeakLoom) | 0 | 2026-04-06 | Application-layer IDS | Name only; distinct scope |
| [pranaveechandra/Leakloom](https://github.com/pranaveechandra/Leakloom) | 0 | 2025-02-01 | Unspecified | Name only |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | 28,199 | 2026-07-19 | Secret detection | Input source, not propagation reporting |
| [mazen160/secrets-patterns-db](https://github.com/mazen160/secrets-patterns-db) | 1,594 | 2026-07-19 | Secret pattern database | Detection primitives only |
| [betterleaks/betterleaks](https://github.com/betterleaks/betterleaks) | 1,487 | 2026-07-19 | Secret scanning | Detection, no evidence timeline |
| [gitleaks/gitleaks-action](https://github.com/gitleaks/gitleaks-action) | 619 | 2026-07-18 | GitHub Action scanner | CI scanner integration |
| [padok-team/git-secret-scanner](https://github.com/padok-team/git-secret-scanner) | 69 | 2026-07-07 | TruffleHog/Gitleaks scanner | Scanner orchestration |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | 36,975 | 2026-07-19 | Supply-chain and secret scanning | Scanner input, much broader scope |
| [aquasecurity/trivy-operator](https://github.com/aquasecurity/trivy-operator) | 1,904 | 2026-07-16 | Kubernetes security toolkit | Runtime/Kubernetes operations |
| [aquasecurity/trivy-action](https://github.com/aquasecurity/trivy-action) | 1,375 | 2026-07-15 | GitHub Action scanner | CI scanning |

## Differentiation decision

The nearest projects detect secrets or schedule scanners. SecretTrail Graph is deliberately narrower: it consumes scanner output plus commit and artifact evidence, correlates a secret via a non-reversible fingerprint, finds an ordered source candidate and recurrence, and delivers a standalone sanitized HTML investigation report. No sampled repository provided the same end-to-end focus, so no further scope reduction was required.

# Stage 0 — Propagation Extension Audit

```json
{
  "role": "V3 PROPAGATION EXTENSION AUDIT",
  "base_model_version": "digital-crystal-v1-frozen",
  "experimental_extension": "digital-crystal-persistent-material-state-v3",
  "canonical_model_modified": false,
  "exact_when_material_state_empty": true,
  "material_extension_exact_reproducibility": true,
  "write_probability": 0.2,
  "modified_neighbor_gain": 0.3,
  "inheritance_probability": 0.5,
  "new_mechanism": "newly attached cells adjacent to pre-existing modified material inherit modified state with fixed probability",
  "interpretation": "Inheritance is local and inert until experience-written modified material exists."
}
```

# MAHAM Scientific Validation

Scientific validation tests whether MAHAM reproduces known analytical results, authoritative numerical data, or published scientific results.

This is distinct from software testing:

- `tests/` verifies that the software behaves as implemented.
- `validation/` verifies that the implementation reproduces expected science.

Published-result validations are stored under `validation/published_results/`.

Each validation should:

- identify the publication and authoritative data source
- use MAHAM's public scientific API rather than internal implementation details
- document the scientific quantities and conventions being checked
- perform numerical checks where possible
- reproduce relevant published trends or figures where appropriate
- clearly report whether the validation passed

Generated validation outputs should not normally be committed unless they serve as intentional reference artifacts.

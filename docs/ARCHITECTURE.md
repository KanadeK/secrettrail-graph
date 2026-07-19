# Architecture

`domain` owns Pydantic models, fingerprinting, masking, and NetworkX-backed timeline construction. It receives raw findings only in memory and returns serializable sanitized models. `adapters` converts tool-specific JSON and writes reports. `services` composes the adapters and core. CLI and FastAPI call the service without containing business rules.

The status calculation compares historical finding fingerprints with a current deterministic workspace scan. A missing current fingerprint is `resolved`; this indicates clean current input, not proof that copies outside the scanned scope are gone.

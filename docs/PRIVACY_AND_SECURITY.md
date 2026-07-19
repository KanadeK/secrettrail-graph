# Privacy and security

SecretTrail Graph never deliberately serializes `FindingInput.secret`. It uses a truncated SHA-256 identifier for correlation and displays only the first and final three characters with a masked middle. HTML escaping is enabled. Treat reports as sensitive operational metadata because locations and dates can still be useful to an attacker.

Run it locally, limit report access, rotate exposed credentials, purge CI logs and artifacts where appropriate, and follow your organization’s evidence-retention policy.

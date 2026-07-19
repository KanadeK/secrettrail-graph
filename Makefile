.PHONY: verify demo package release-check

verify:
	python scripts/verify.py

demo:
	python -m leakloom.cli analyze --gitleaks examples/gitleaks.json --trivy examples/trivy.json --git-log examples/git-log.json --artifacts examples/artifacts.json --workspace examples/current --html dist-release/demo-report.html --json dist-release/demo-report.json

package:
	python scripts/package_release.py

release-check:
	python scripts/release_check.py

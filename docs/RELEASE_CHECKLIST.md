# Release checklist

- `make verify`, `make demo`, and `make package` pass.
- `make release-check` passes from a clean worktree.
- Check report output for raw sample values.
- Verify local author and committer match the authenticated GitHub account.
- Push `main`, wait for green CI, then create the annotated tag and GitHub release.

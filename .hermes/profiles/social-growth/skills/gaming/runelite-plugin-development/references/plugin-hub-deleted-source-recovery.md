# Recovering a deleted source repository for an officially merged RuneLite plugin

Use this when a Plugin Hub marker still exists but its source repository returns 404 and the completed lifecycle checkout is missing.

## Recovery standard

1. Resolve the authoritative Plugin Hub marker and merged PR first. Record:
   - marker filename;
   - canonical repository URL;
   - immutable accepted commit;
   - merged PR and merge state.
2. Search local completed paths and project backups for a real Git repository or `.bundle`. Never reconstruct or fabricate accepted source from screenshots, PR patches, or descriptions.
3. For a bundle, verify both integrity and accepted-object presence:
   ```bash
   git bundle verify /path/project.bundle
   git bundle list-heads /path/project.bundle
   git clone /path/project.bundle /tmp/project-verify
   git -C /tmp/project-verify cat-file -t <accepted-sha>
   git -C /tmp/project-verify show -s --format='%H %s' <accepted-sha>
   ```
   Require complete history and the exact accepted commit.
4. Clone the verified history into `projects/osrs-plugins/completed/<Plugin>`, set the canonical GitHub remote, and build from that checkout with Java 11. If historical `gradlew` lacks execute permission, use `bash ./gradlew ...` rather than dirtying the accepted revision merely to change the mode.
5. If the canonical GitHub repository is truly absent, recreate the exact public repository and push the recovered branch/history unchanged. Verify `git ls-remote` equals the accepted marker SHA. This repairs the Plugin Hub marker rather than silently creating a differently named replacement.
6. Register the restored checkout as a real HeRmEz submodule:
   - add `.gitmodules` path, URL, and branch;
   - run `git submodule absorbgitdirs` for an existing nested checkout;
   - verify index mode `160000` and exact accepted SHA.
7. If the parent checkout is dirty or diverged, commit the narrow local lifecycle change for local continuity, but publish the equivalent `.gitmodules` + gitlink change from an isolated clone based on remote `main`. Verify the remote parent SHA and stored gitlink afterward.
8. Re-run the GitHub OSRS repository inventory. Keep officially merged plugin sources even if seasonal or no longer under active feature development; their source repositories remain part of Plugin Hub integrity.

## Cleanup boundary

Repository recovery and repository deletion are different operations. After recovery, classify all OSRS repositories into active, pending-review, completed, service/infrastructure, template, and Plugin Hub fork. Present exact deletion candidates and obtain confirmation before deletion. A completed official plugin source is not an abandonment candidate solely because development is inactive.

## Verification checklist

- Plugin Hub marker resolves the restored canonical URL.
- Accepted SHA exists locally and remotely.
- Java 11 clean test/assemble succeeds.
- Restored child worktree is clean.
- HeRmEz `.gitmodules` and `160000` gitlink use the completed path.
- Remote HeRmEz main stores the exact accepted child SHA.

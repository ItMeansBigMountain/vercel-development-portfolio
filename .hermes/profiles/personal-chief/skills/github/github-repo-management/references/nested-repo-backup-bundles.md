# Nested repo project backups in HeRmEz

Use this pattern when an active project lives inside `/opt/data/HeRmEz/projects/<project>` and is itself a Git repository, but the user also wants a backup committed to the private HeRmEz workspace repo.

## Layout

```text
/opt/data/HeRmEz/projects/<project>/                 # active worktree; usually ignored by parent repo
/opt/data/HeRmEz/projects/_backups/<project>/
  <project>.bundle                                   # Git bundle committed to HeRmEz
  README.md                                          # restore metadata committed to HeRmEz
```

## Commands

```bash
PARENT=/opt/data/HeRmEz
PROJECT=<project>
CHILD="$PARENT/projects/$PROJECT"
BACKUP_DIR="$PARENT/projects/_backups/$PROJECT"
mkdir -p "$BACKUP_DIR"

SHA=$(git -C "$CHILD" rev-parse HEAD)
BRANCH=$(git -C "$CHILD" branch --show-current)
REMOTE=$(git -C "$CHILD" remote get-url origin)

git -C "$CHILD" status --short
git -C "$CHILD" bundle create "$BACKUP_DIR/$PROJECT.bundle" --all
cat > "$BACKUP_DIR/README.md" <<EOF
# $PROJECT backup

- Project path: \`$CHILD\`
- Source remote at backup time: \`$REMOTE\`
- Branch at backup time: \`$BRANCH\`
- Latest commit at backup time: \`$SHA\`
- Backup file: \`projects/_backups/$PROJECT/$PROJECT.bundle\`

## Restore

\`\`\`bash
git bundle verify projects/_backups/$PROJECT/$PROJECT.bundle
git clone projects/_backups/$PROJECT/$PROJECT.bundle restored-$PROJECT
\`\`\`
EOF

cd "$PARENT"
git bundle verify "projects/_backups/$PROJECT/$PROJECT.bundle"
rm -rf "/tmp/${PROJECT}-restore-check"
git clone "projects/_backups/$PROJECT/$PROJECT.bundle" "/tmp/${PROJECT}-restore-check"
git -C "/tmp/${PROJECT}-restore-check" log -1 --oneline
```

## Parent `.gitignore`

Ignore the active nested worktree but not `projects/_backups/`:

```gitignore
# Git internals from nested repos/backups
**/.git/

# Active nested project worktrees are backed up as Git bundles under /projects/_backups/
/projects/<project>/
```

## Pitfalls

- A Git bundle captures committed history only. Commit or explicitly report dirty child worktree changes before bundling.
- Do not track local DBs, uploaded media, `.env`, caches, or nested `.git` internals in the parent repo.
- Verify restore from the exact backup path before telling the user it is safe.

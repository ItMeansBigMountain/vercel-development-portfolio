# Kanban SQLite index integrity repair

Use when `hermes kanban ...` refuses to initialize because SQLite `PRAGMA integrity_check` reports index-only corruption such as:

- `wrong # of entries in index idx_events_run`
- `wrong # of entries in index idx_events_task`

This usually means the table data may still be readable, but one or more secondary indexes need rebuilding.

## Safe recovery pattern

1. **Back up the DB first** before any repair:

```python
import pathlib, shutil, time
p = pathlib.Path('/opt/data/kanban.db')
backup = p.with_suffix(f'.db.pre_reindex_{int(time.time())}.bak')
shutil.copy2(p, backup)
print(backup)
```

2. **Run REINDEX for the named failing indexes** and verify integrity:

```python
import sqlite3
p = '/opt/data/kanban.db'
con = sqlite3.connect(p)
cur = con.cursor()
for index_name in ['idx_events_run', 'idx_events_task']:
    cur.execute(f'REINDEX {index_name}')
con.commit()
print(cur.execute('PRAGMA integrity_check').fetchall())
```

3. **Re-run the Kanban command** that failed, e.g.:

```bash
HERMES_KANBAN_BOARD=default hermes kanban list
```

## Guardrails

- Only use this pattern when integrity output names indexes, not when table pages/data are corrupted.
- Never delete or replace the DB before taking a timestamped backup.
- If `PRAGMA integrity_check` still reports non-index corruption after `REINDEX`, stop and restore/repair from backup rather than forcing more writes.
- Treat this as a recovery step for the board, not as task progress; after repair, inspect the board normally and report the actual next card/status.

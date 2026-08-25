# RuneLite local run + push handoff notes

Use when Hermes edits a standalone RuneLite plugin repo but the user will run it from their Windows workspace.

## Local run command handoff

If the user says they want to run the plugin locally, prefer giving the command instead of launching the Linux-side client unless they explicitly ask Hermes to run it:

```powershell
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\<PluginRepo>
.\gradlew.bat run --no-daemon
```

If Java 11 is not selected:

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat run --no-daemon
```

## Push-before-user-pulls pattern

Before telling the user to pull locally:

1. Run `./gradlew clean test assemble --no-daemon --console=plain` with Java 11.
2. Commit the child plugin repo changes.
3. Push the child plugin repo to `origin main`.
4. Verify remote head with `git ls-remote origin refs/heads/main` and compare it to `git log --oneline -1`.

If HTTPS push prompts for credentials in the agent environment but `GITHUB_ACCESS_TOKEN` is configured, push via token without printing it. Keep command output token-redacted.

## Windows detached HEAD recovery

The user's local plugin repo may be checked out as a submodule-style detached HEAD, causing plain `git pull` to fail with:

```text
You are not currently on a branch.
Please specify which branch you want to merge with.
```

After the remote push is verified, tell the user:

```bat
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\<PluginRepo>
git switch main
git pull origin main
```

If `git switch main` reports local changes, stop and inspect/ask before suggesting force commands.

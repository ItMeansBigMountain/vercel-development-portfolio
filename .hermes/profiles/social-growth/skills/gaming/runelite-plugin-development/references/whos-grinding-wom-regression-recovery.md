# Who's Grinding Panel: WOM regression recovery

Session lesson from a broken fallback/search pass: when the panel starts showing only `Official hiscores baseline saved` for players that previously had WOM stats (e.g. `oyama`), treat it as a WOM-primary regression and restore the last known WOM-working commit before further feature work.

## Known-good checkpoint from this session

The last commit verified as a WOM-working baseline before official-hiscores fallback changes was:

```text
a0e2162 feat: add player header and OSRS acronym labels
```

This point is before the official hiscores fallback commits that made the card prefer/show baseline messages:

```text
4ba314d feat: fall back to official hiscores snapshots
48c6d0f feat: add official hiscores gains fallback
```

If reverting a local/remote plugin repo to this baseline, verify with:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

Then verify WOM itself for a known player before adding fallback/search again:

```bash
python3 - <<'PY'
import urllib.request, urllib.parse, json
name='oyama'
url='https://api.wiseoldman.net/v2/players/'+urllib.parse.quote(name)+'/gained?period=week'
req=urllib.request.Request(url, headers={'User-Agent':'WhosGrindingPanel RuneLite plugin','Accept':'application/json'})
with urllib.request.urlopen(req, timeout=15) as r:
    data=json.load(r)
print('has_data', bool(data.get('data')))
skills=data.get('data',{}).get('skills',{})
print([(k,v.get('experience',{}).get('gained',0)) for k,v in skills.items() if v.get('experience',{}).get('gained',0)>0][:8])
PY
```

## Recovery sequence

1. Stop adding features on top of a broken data path.
2. Identify the last commit where WOM stats rendered in the card.
3. Reset/revert the plugin repo to that point and run tests/build.
4. Verify live WOM separately for a known player such as `oyama` with the same User-Agent headers the plugin uses.
5. Push the child plugin repo first, then update/push the HeRmEz parent submodule pointer.
6. Re-add features one at a time: search UI first, then fallback, with a build and live WOM smoke test after each.

## Design rule after regression

Do not let official hiscores fallback mask WOM failures. If WOM returns data for a known player, the card should render WOM gains even if local official-hiscore baselines are missing. Fallback should be used only after WOM genuinely fails or has no positive gains, and fallback work should not change the WOM fetch/update sequence in the same pass unless explicitly tested.

## Console command preference

When the user asks for the RuneLite run command and wants only errors visible, provide the concise Windows command only:

```bat
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\pr-review-pending\WhosGrindingClanPanel
.\gradlew.bat run --no-daemon --console=plain --quiet 1>NUL
```

Avoid extra explanation when the user asks for “the command only.”

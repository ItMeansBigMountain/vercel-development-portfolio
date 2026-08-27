#!/usr/bin/env python3
import concurrent.futures
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import urllib.error
import urllib.request
from collections import Counter, defaultdict

ROOT = pathlib.Path('/opt/data/HeRmEz')
OUT = ROOT / 'projects/_ops/portfolio-audit'
SOURCE = pathlib.Path('/opt/data/cache/documents/doc_76d816784680_message.txt')
UA = 'Hermes-Portfolio-Audit/1.0'

def request_json(url, token=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': UA}
    if token:
        headers['Authorization'] = f'Bearer {token}'
        headers['X-GitHub-Api-Version'] = '2022-11-28'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.load(response), dict(response.headers)
    except urllib.error.HTTPError as exc:
        try:
            body = json.load(exc)
        except Exception:
            body = {'message': str(exc)}
        return exc.code, body, dict(exc.headers)

def github_inventory():
    token = os.environ.get('GITHUB_ACCESS_TOKEN') or os.environ.get('GITHUB_TOKEN')
    repos = []
    statuses = []
    for page in range(1, 20):
        status, body, _ = request_json(
            f'https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner,collaborator,organization_member&sort=updated', token
        )
        statuses.append(status)
        if status != 200:
            message = body.get('message') if isinstance(body, dict) else 'Unexpected GitHub API response'
            return {'api_statuses': statuses, 'error': {'status': status, 'message': message}, 'repos': repos}
        if not isinstance(body, list):
            return {'api_statuses': statuses, 'error': {'status': status, 'message': 'GitHub repository response was not a list'}, 'repos': repos}
        if not body:
            break
        for source_repo in body:
            repo = {k: source_repo.get(k) for k in ('full_name','name','private','archived','fork','html_url','updated_at','default_branch','description','homepage','language')}
            owner = source_repo.get('owner')
            repo['owner'] = owner.get('login') if isinstance(owner, dict) else owner
            repos.append(repo)
        if len(body) < 100:
            break
    return {'api_statuses': statuses, 'repos': repos}

def vercel_diagnostic():
    token = os.environ.get('VERCEL_API_TOKEN')
    result = {'token_present': bool(token), 'probes': []}
    for path in ('/v2/user','/v2/teams','/v9/projects'):
        headers = {'User-Agent': UA}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        req = urllib.request.Request('https://api.vercel.com' + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = json.load(response)
                result['probes'].append({'path': path, 'status': response.status, 'error': None, 'body_keys': sorted(body)})
        except urllib.error.HTTPError as exc:
            try:
                body = json.load(exc)
            except Exception:
                body = {}
            error = body.get('error', body)
            result['probes'].append({'path': path, 'status': exc.code, 'error': {k: error.get(k) for k in ('code','message','invalidToken') if k in error}})
    invalid = bool(result['probes']) and all(p['status'] == 403 and p.get('error', {}).get('invalidToken') is True for p in result['probes'])
    result['diagnosis'] = 'VERCEL_API_TOKEN is rejected by Vercel as invalid/not authorized on every tested identity, team, and project endpoint.' if invalid else 'See per-endpoint results; no broader credential conclusion made.'
    result['next_action'] = 'Create a fresh Vercel access token for the intended account/team, replace VERCEL_API_TOKEN in the secret store, then rerun this audit; do not paste the token into Kanban or logs.' if invalid else 'Review endpoint results and account/team scope before changing credentials.'
    return result

def parse_targets():
    text = SOURCE.read_text()
    entries = []
    for line in text.splitlines():
        match = re.search(r'https://[^\s)]+', line)
        if not match:
            continue
        url = match.group(0).rstrip('/').rstrip('.') + '/'
        label = re.sub(r'^.*?\|', '', line).split('—')[0].strip()
        entries.append({'label': label, 'url': url})
    return entries

def probe(entry):
    req = urllib.request.Request(entry['url'], headers={'User-Agent': UA}, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            sample = response.read(65536).decode('utf-8', 'replace')
            title = re.search(r'<title[^>]*>(.*?)</title>', sample, re.I | re.S)
            return {**entry, 'status': response.status, 'final_url': response.geturl(), 'title': re.sub(r'\s+', ' ', title.group(1)).strip() if title else None, 'reachable': 200 <= response.status < 400}
    except urllib.error.HTTPError as exc:
        return {**entry, 'status': exc.code, 'final_url': exc.geturl(), 'title': None, 'reachable': False}
    except Exception as exc:
        reason = getattr(exc, 'reason', None)
        return {**entry, 'status': None, 'final_url': None, 'title': None, 'reachable': False, 'error_type': type(exc).__name__, 'error': str(reason or exc)}

def local_inventory():
    modules = []
    gm = (ROOT / '.gitmodules').read_text()
    current = {}
    for line in gm.splitlines():
        if line.startswith('[submodule '):
            if current: modules.append(current)
            current = {'name': line.split('"')[1]}
        elif '=' in line:
            key, value = [x.strip() for x in line.split('=', 1)]
            current[key] = value
    if current: modules.append(current)
    projects = []
    base = ROOT / 'projects'
    for child in sorted(base.iterdir(), key=lambda p: p.name.lower()):
        if child.is_dir():
            projects.append(str(child.relative_to(ROOT)))
    return {'submodules': modules, 'top_level_project_dirs': projects}

def normalized(value):
    return re.sub(r'[^a-z0-9]', '', value.lower())

def main():
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    github = github_inventory()
    targets = parse_targets()
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        probes = list(pool.map(probe, targets))
    local = local_inventory()
    local_names = {normalized(pathlib.Path(p).name): p for p in local['top_level_project_dirs']}
    sub_by_url = {m.get('url','').removesuffix('.git').lower(): m.get('path') for m in local['submodules']}
    for repo in github['repos']:
        repo['local_matches'] = sorted(set(filter(None, [local_names.get(normalized(repo['name'])), sub_by_url.get(repo['html_url'].lower())])))
    repo_names = defaultdict(list)
    for repo in github['repos']:
        repo_names[normalized(repo['name'])].append(repo['full_name'])
    for deployment in probes:
        deployment['repository_candidates'] = repo_names.get(normalized(deployment['label']), [])
    groups = [
        {'canonical': 'Coding School', 'members': ['Coding School','Algorithm Academy/Algos','School'], 'target': 'https://coding-school-platform.vercel.app/'},
        {'canonical': 'Journal product (decision unresolved)', 'members': ['Journal AI','Journal App'], 'target': None},
        {'canonical': 'Music product (decision unresolved)', 'members': ['MusicAI','Music','Music Mood'], 'target': None},
        {'canonical': 'Local Meeting Transcriber', 'members': ['Local Meeting Transcriber','Local Meeting Transcriber shell'], 'target': 'https://local-meeting-transcriber-frontend.vercel.app/'},
        {'canonical': 'API Requests (decision unresolved)', 'members': ['API Requests','API.Requests'], 'target': None},
        {'canonical': 'TicVoter', 'members': ['TicVoter','TicVoter REST API'], 'target': None, 'note': 'Related frontend/API pair, not necessarily duplicates.'},
        {'canonical': 'Muscle Madness', 'members': ['Muscle Madness','Muscle Madness API'], 'target': None, 'note': 'Related frontend/API pair, not necessarily duplicates.'},
    ]
    owner_counts = Counter(r['owner'] for r in github['repos'])
    summary = {
        'github_visible_repos': len(github['repos']),
        'github_owner_counts': dict(sorted(owner_counts.items())),
        'github_archived': sum(bool(r['archived']) for r in github['repos']),
        'github_private': sum(bool(r['private']) for r in github['repos']),
        'github_forks': sum(bool(r['fork']) for r in github['repos']),
        'github_with_local_match': sum(bool(r['local_matches']) for r in github['repos']),
        'listed_deployments': len(probes),
        'reachable_deployments': sum(p['reachable'] for p in probes),
        'unreachable_deployments': sum(not p['reachable'] for p in probes),
        'http_status_counts': dict(sorted(Counter(str(p['status']) for p in probes).items())),
        'submodules': len(local['submodules']),
        'top_level_project_dirs': len(local['top_level_project_dirs']),
    }
    artifact = {'schema_version': 1, 'generated_at': generated, 'source_document': str(SOURCE), 'safety': 'Audit only; no repository or deployment state was changed.', 'summary': summary, 'vercel_api': vercel_diagnostic(), 'duplicate_or_related_groups': groups, 'deployments': probes, 'github': github, 'local': local}
    (OUT / 'inventory.json').write_text(json.dumps(artifact, indent=2) + '\n')
    lines = ['# Portfolio inventory', '', f'Generated: {generated}', '', 'Audit only: no repository or deployment state was changed.', '', '## Verified counts', '']
    for key, value in summary.items(): lines.append(f'- {key.replace("_", " ")}: {value}')
    lines += ['', '## Vercel credential blocker', '', f'- {artifact["vercel_api"]["diagnosis"]}', f'- Next: {artifact["vercel_api"]["next_action"]}', '', '## Deployment probes', '']
    for p in probes:
        status = p['status'] if p['status'] is not None else p.get('error_type', 'error')
        title = f' — {p["title"]}' if p.get('title') else ''
        lines.append(f'- {p["label"]}: HTTP {status} — {p["url"]}{title}')
    lines += ['', '## Duplicate or related groups', '']
    for group in groups:
        target = group['target'] or 'canonical target unresolved'
        lines.append(f'- {group["canonical"]}: {", ".join(group["members"])} → {target}')
        if group.get('note'): lines.append(f'  - {group["note"]}')
    lines += ['', '## GitHub inventory', '']
    for repo in github['repos']:
        flags = ', '.join(x for x, yes in [('private',repo['private']),('archived',repo['archived']),('fork',repo['fork'])] if yes) or 'public, active, source'
        local_match = f'; local: {", ".join(repo["local_matches"])}' if repo['local_matches'] else ''
        lines.append(f'- {repo["full_name"]}: {flags}; updated {repo["updated_at"]}{local_match} — {repo["html_url"]}')
    lines += ['', '## Ownership and interpretation', '', '- Repository ownership is the API-reported owner namespace; visibility does not imply sole ownership.', '- Deployment ownership/project IDs remain unverified while the Vercel credential is rejected. Public URL reachability proves serving state only, not account ownership.', '- Consolidation groups are duplicate/relationship candidates. No merge, archive, delete, or dehost action was performed.', '', 'Machine-readable detail: `inventory.json`']
    (OUT / 'INVENTORY.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()

"""Fresh MD planning files and provenance checks. No molecular execution API.

This audits declared files/coverage, not chemistry, scientific reasoning or
test semantics. A successful check never constitutes runtime authorization.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

SKILL = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    def bad(value):
        raise ValueError('nonfinite JSON number: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'),
        object_pairs_hook=unique_object, parse_constant=bad)


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False) + '\n', encoding='utf-8')


def scope_id(system_id, inputs):
    return digest({'system_id': system_id, 'inputs': inputs})


def initialize(system_id, inputs, output):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', system_id):
        raise ValueError('system ID must be 1-80 ASCII letters/digits/_/-')
    paths = [Path(p).resolve(strict=True) for p in inputs]
    if not paths or len(set(paths)) != len(paths) or not all(p.is_file() for p in paths):
        raise ValueError('provide distinct existing input files')
    files = [{'path': str(p), 'sha256': sha(p)} for p in paths]
    out = Path(output).resolve()
    if out.exists():
        raise ValueError('refusing to overwrite an existing plan directory')
    # Read templates before creating output; no case data or runtime is imported.
    templates = {name: (SKILL / 'assets' / source).read_text(encoding='utf-8')
        for name, source in [('A.md', 'system-decision-card.md'),
                             ('B.md', 'md-plan-card.md'),
                             ('system-assessment.md', 'new-system-assessment.md')]}
    scope = scope_id(system_id, files)
    out.mkdir(parents=True, exist_ok=False)
    for name, body in templates.items():
        (out / name).write_text(f'<!-- system_id={system_id}; scope_sha256={scope}; unconfirmed -->\n\n' + body, encoding='utf-8')
    record = {'schema': 'md-new-system-1', 'system_id': system_id,
        'scope_sha256': scope, 'inputs': files,
        'assessment': {'path': 'system-assessment.md', 'sha256': None},
        'cards': {k: {'path': k + '.md', 'sha256': None} for k in ('A', 'B')},
        'configuration': None, 'parameter_decisions': [],
        'implementation': {'status': 'not_assessed', 'files': [], 'coverage': []}}
    write(out / 'adaptation.json', record)
    return {'created': str(out), 'scope_sha256': scope,
        'parameter_defaults_created': False, 'runtime_authorized': False}


def leaves(value, pointer=''):
    if isinstance(value, dict) and value:
        for key, child in value.items():
            key = key.replace('~', '~0').replace('/', '~1')
            yield from leaves(child, pointer + '/' + key)
    elif isinstance(value, list) and value:
        for i, child in enumerate(value):
            yield from leaves(child, pointer + '/' + str(i))
    else:
        yield pointer, value


def check(record_path):
    base = Path(record_path).resolve().parent
    record = read(record_path)
    issues, implementation_issues = [], []

    def need(ok, message, bucket=issues):
        if not ok:
            bucket.append(message)

    def bound_file(item, label, bucket=issues):
        if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not item['path']:
            bucket.append(label + ': missing path/hash'); return None
        path = (base / item['path']).resolve()
        if not path.is_file():
            bucket.append(label + ': file missing'); return None
        actual = sha(path)
        need(actual == item.get('sha256'), label + ': missing/stale SHA256', bucket)
        return actual

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    need(record.get('schema') == 'md-new-system-1', 'wrong schema')
    need(text(record.get('system_id')), 'missing system_id')
    inputs = record.get('inputs', [])
    need(isinstance(inputs, list) and bool(inputs), 'no current input files')
    current = []
    for item in inputs:
        actual = bound_file(item, 'input')
        current.append({'path': str((base / item['path']).resolve()), 'sha256': actual})
    need(len({x['path'] for x in current}) == len(current), 'duplicate inputs')
    scope = scope_id(record.get('system_id'), current)
    need(scope == record.get('scope_sha256'), 'scope mismatch: new input/system requires reassessment')
    assessment = bound_file(record.get('assessment'), 'assessment')
    cards = record.get('cards', {})
    card_hashes = {k: bound_file(cards.get(k), 'card ' + k) for k in ('A', 'B')}
    decision_context = digest({'scope_sha256': scope, 'assessment_sha256': assessment, 'A_card_sha256': card_hashes['A']})
    config_hash = bound_file(record.get('configuration'), 'configuration')
    config = read(base / record['configuration']['path']) if config_hash else {}
    need(isinstance(config, dict) and bool(config), 'configuration must be a nonempty JSON object')
    values = dict(leaves(config)) if isinstance(config, dict) and config else {}
    value_hashes = {key: digest(value) for key, value in values.items()}
    decisions = record.get('parameter_decisions', [])
    seen = set()
    for row in decisions:
        pointer = row.get('pointer')
        need(pointer in values and pointer not in seen, 'unknown/duplicate decision: ' + str(pointer))
        seen.add(pointer)
        need(row.get('scope_sha256') == scope, 'old/missing decision scope: ' + str(pointer))
        need(row.get('decision_context_sha256') == decision_context, 'assessment/A changed or unbound: ' + str(pointer))
        need(row.get('value_sha256') == value_hashes.get(pointer), 'parameter value changed/unreviewed: ' + str(pointer))
        need(row.get('origin') in ('new_decision', 'reassessed'), 'unreviewed/default origin: ' + str(pointer))
        if row.get('origin') == 'reassessed':
            need(text(row.get('previous_source')), 'missing previous source: ' + str(pointer))
        for key in ('source', 'rationale', 'validation', 'failure_action'):
            need(text(row.get(key)), 'missing ' + key + ': ' + str(pointer))
    need(seen == set(values), 'configuration fields lack decisions: ' + str(sorted(set(values) - seen)))

    impl = record.get('implementation', {})
    need(impl.get('status') == 'adapted', 'current-system implementation is not adapted', implementation_issues)
    code_files = []
    for item in impl.get('files', []):
        actual = bound_file(item, 'implementation', implementation_issues)
        code_files.append({'path': str((base / item['path']).resolve()), 'sha256': actual})
    need(bool(code_files), 'no current implementation files', implementation_issues)
    context = digest({'decision_context_sha256': decision_context, 'B_card_sha256': card_hashes['B'],
        'configuration_sha256': config_hash, 'files': sorted(code_files, key=lambda x: x['path'])})
    covered = set()
    for row in impl.get('coverage', []):
        pointer = row.get('pointer')
        need(pointer in values and pointer not in covered, 'unknown/duplicate implementation field: ' + str(pointer), implementation_issues)
        covered.add(pointer)
        need(text(row.get('consumer')), 'missing consuming function/option: ' + str(pointer), implementation_issues)
        need(row.get('context_sha256') == context, 'implementation verification context changed/unbound: ' + str(pointer), implementation_issues)
        bound_file(row.get('evidence'), 'verification ' + str(pointer), implementation_issues)
    need(covered == set(values), 'unimplemented/unverified fields: ' + str(sorted(set(values) - covered)), implementation_issues)
    return {'parameter_provenance_complete': not issues,
        'static_handoff_complete': not (issues or implementation_issues),
        'issues': issues, 'implementation_issues': implementation_issues,
        'expected_scope_sha256': scope, 'expected_decision_context_sha256': decision_context,
        'expected_implementation_context_sha256': context, 'expected_value_sha256': value_hashes,
        'runtime_authorized': False,
        'limit': 'File/declared coverage audit only. Scientific reasoning, card/config semantics and actual test contents require review; no molecular execution or authorization.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init'); init.add_argument('--system-id', required=True)
    init.add_argument('--input', action='append', required=True); init.add_argument('--out', required=True)
    audit = sub.add_parser('check'); audit.add_argument('record')
    args = parser.parse_args()
    try:
        result = initialize(args.system_id, args.input, args.out) if args.command == 'init' else check(args.record)
        status = 0 if args.command == 'init' or result['static_handoff_complete'] else 2
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        result = {'error': str(exc), 'runtime_authorized': False}; status = 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return status


if __name__ == '__main__':
    raise SystemExit(main())

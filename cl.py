#!/usr/bin/env python3
"""CL prototype — steps 1-4: identity, contributions, confirmations, integrity."""

import argparse
import base64
import hashlib
import json
import sqlite3
import sys
import time
from pathlib import Path

from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

KEYS_DIR = Path(".cl-keys")
DB_PATH = Path("cl.db")

MAX_WEIGHT = 1000.0
MAX_FUTURE_SKEW_SEC = 300  # 5 minutes


def b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def unb64(s: str) -> bytes:
    padding = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def compute_event_id(event: dict) -> str:
    h = hashlib.sha256(canonical_json(event)).hexdigest()
    return f"sha256:{h}"


def confirm_payload(contribution_id: str, confirmer_did: str) -> bytes:
    return f"confirm:{contribution_id}:{confirmer_did}".encode()


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            author TEXT NOT NULL,
            context TEXT NOT NULL,
            action TEXT NOT NULL,
            weight REAL NOT NULL,
            note TEXT,
            created_at INTEGER NOT NULL,
            signature TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS confirmations (
            contribution_id TEXT NOT NULL,
            confirmer TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            signature TEXT NOT NULL,
            PRIMARY KEY (contribution_id, confirmer),
            FOREIGN KEY (contribution_id) REFERENCES events(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_author ON events(author)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_context ON events(context)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_confirmations_contrib ON confirmations(contribution_id)")
    conn.commit()
    return conn


def load_key(name: str):
    key_file = KEYS_DIR / f"{name}.json"
    if not key_file.exists():
        print(f"error: no key named '{name}' (run: python cl.py keygen {name})")
        sys.exit(1)
    data = json.loads(key_file.read_text())
    sk = SigningKey(unb64(data["private_key"]))
    return data["did"], sk


def did_to_verify_key(did: str) -> VerifyKey:
    parts = did.split(":")
    if len(parts) != 4 or parts[0] != "did" or parts[1] != "cl":
        raise ValueError(f"bad did: {did}")
    return VerifyKey(unb64(parts[3]))


def event_from_row(row) -> dict:
    """Восстанавливает событие из строки БД в том же виде, в каком оно было подписано."""
    return {
        "type": row[1],
        "author": row[2],
        "context": row[3],
        "action": row[4],
        "weight": row[5],
        "note": row[6],
        "created_at": row[7],
    }


def check_event(row) -> tuple[bool, str]:
    """
    Проверяет, что событие в БД не подделано.
    Возвращает (True, '') если всё ок, (False, reason) если нет.
    """
    eid, _type, author, _context, _action, _weight, _note, _created, signature = row

    # 1. Пересчитываем ID из полей. Если не совпало — данные менялись.
    event = event_from_row(row)
    recomputed = compute_event_id(event)
    if recomputed != eid:
        return False, "id mismatch (event data was modified)"

    # 2. Проверяем подпись.
    try:
        vk = did_to_verify_key(author)
        vk.verify(eid.encode(), unb64(signature))
    except (BadSignatureError, ValueError):
        return False, "bad signature"

    return True, ""


def check_confirmation(row) -> tuple[bool, str]:
    contribution_id, confirmer, _created, signature = row
    try:
        vk = did_to_verify_key(confirmer)
        vk.verify(confirm_payload(contribution_id, confirmer), unb64(signature))
    except (BadSignatureError, ValueError):
        return False, "bad confirmation signature"
    return True, ""


def cmd_keygen(args):
    KEYS_DIR.mkdir(exist_ok=True)
    key_file = KEYS_DIR / f"{args.name}.json"

    if key_file.exists() and not args.force:
        print(f"error: {key_file} already exists (use --force to overwrite)")
        sys.exit(1)

    sk = SigningKey.generate()
    pub_b64 = b64(bytes(sk.verify_key))
    did = f"did:cl:dev:{pub_b64}"

    key_file.write_text(json.dumps({
        "name": args.name,
        "did": did,
        "public_key": pub_b64,
        "private_key": b64(bytes(sk)),
    }, indent=2))
    key_file.chmod(0o600)

    print(f"created: {key_file}")
    print(f"did:     {did}")


def cmd_add_contribution(args):
    # Валидация входа
    if args.weight <= 0:
        print("error: weight must be > 0")
        sys.exit(1)
    if args.weight > MAX_WEIGHT:
        print(f"error: weight must be <= {MAX_WEIGHT}")
        sys.exit(1)
    if not args.context.strip():
        print("error: context cannot be empty")
        sys.exit(1)
    if not args.action.strip():
        print("error: action cannot be empty")
        sys.exit(1)

    now = int(time.time())
    did, sk = load_key(args.name)

    event = {
        "type": "contribution.create",
        "author": did,
        "context": args.context,
        "action": args.action,
        "weight": float(args.weight),
        "note": args.note or "",
        "created_at": now,
    }
    eid = compute_event_id(event)
    signature = b64(bytes(sk.sign(eid.encode()).signature))

    conn = db()
    try:
        conn.execute(
            "INSERT INTO events (id, type, author, context, action, weight, note, created_at, signature) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (eid, event["type"], event["author"], event["context"], event["action"],
             event["weight"], event["note"], event["created_at"], signature),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("error: identical event already exists")
        sys.exit(1)
    finally:
        conn.close()

    print(f"added:   {eid}")
    print(f"author:  {did}")
    print(f"context: {args.context}")
    print(f"action:  {args.action}  weight={args.weight}")


def cmd_confirm(args):
    now = int(time.time())
    did, sk = load_key(args.name)

    conn = db()
    row = conn.execute(
        "SELECT id, type, author, context, action, weight, note, created_at, signature "
        "FROM events WHERE id = ?",
        (args.contribution_id,),
    ).fetchone()
    if not row:
        print(f"error: no such contribution: {args.contribution_id}")
        conn.close()
        sys.exit(1)

    ok, reason = check_event(row)
    if not ok:
        print(f"error: cannot confirm: event is invalid ({reason})")
        conn.close()
        sys.exit(1)

    author = row[2]
    if author == did:
        print("error: you cannot confirm your own contribution")
        conn.close()
        sys.exit(1)

    payload = confirm_payload(args.contribution_id, did)
    signature = b64(bytes(sk.sign(payload).signature))

    try:
        conn.execute(
            "INSERT INTO confirmations (contribution_id, confirmer, created_at, signature) "
            "VALUES (?, ?, ?, ?)",
            (args.contribution_id, did, now, signature),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("error: you already confirmed this contribution")
        conn.close()
        sys.exit(1)
    finally:
        conn.close()

    print(f"confirmed: {args.contribution_id}")
    print(f"by:        {did}")


def cmd_list(args):
    conn = db()
    rows = conn.execute(
        """
        SELECT id, type, author, context, action, weight, note, created_at, signature
        FROM events ORDER BY created_at
        """
    ).fetchall()
    confirms = conn.execute(
        "SELECT contribution_id, confirmer FROM confirmations"
    ).fetchall()
    conn.close()

    if not rows:
        print("(no events)")
        return

    conf_counts = {}
    for cid, _conf in confirms:
        conf_counts[cid] = conf_counts.get(cid, 0) + 1

    for row in rows:
        eid, _type, _author, context, action, weight, note, _created, _sig = row
        ok, reason = check_event(row)
        n_conf = conf_counts.get(eid, 0)

        if ok:
            status = f"confirmed×{n_conf}" if n_conf else "pending"
        else:
            status = f"INVALID:{reason[:12]}"

        print(f"{eid[:20]}...  {context:18s}  {action:12s}  w={weight:<4}  [{status:18s}]  {note}")


def cmd_verify(args):
    conn = db()
    events = conn.execute(
        "SELECT id, type, author, context, action, weight, note, created_at, signature FROM events"
    ).fetchall()
    confirms = conn.execute(
        "SELECT contribution_id, confirmer, created_at, signature FROM confirmations"
    ).fetchall()
    conn.close()

    bad = 0
    for row in events:
        ok, reason = check_event(row)
        if not ok:
            print(f"BAD event: {row[0][:24]}...  ({reason})")
            bad += 1

    for row in confirms:
        ok, reason = check_confirmation(row)
        if not ok:
            print(f"BAD confirmation: {row[0][:24]}... by {row[1][:24]}...  ({reason})")
            bad += 1

    total = len(events) + len(confirms)
    if bad == 0:
        print(f"ok: {total} signatures verified")
    else:
        print(f"FAILED: {bad} of {total} invalid")
        sys.exit(1)


def cmd_reputation(args):
    """
    Репутация считается ТОЛЬКО по валидным событиям и ТОЛЬКО по валидным подтверждениям.
    """
    conn = db()
    event_rows = conn.execute(
        "SELECT id, type, author, context, action, weight, note, created_at, signature FROM events"
    ).fetchall()
    confirm_rows = conn.execute(
        "SELECT contribution_id, confirmer, created_at, signature FROM confirmations"
    ).fetchall()
    conn.close()

    # Фильтруем: только валидные события
    valid_events = {}
    for row in event_rows:
        ok, _ = check_event(row)
        if ok:
            eid, _type, author, context, _action, weight, _note, _created, _sig = row
            valid_events[eid] = (author, context, weight)

    # Фильтруем: только валидные подтверждения, ссылающиеся на валидные события
    confirmed_ids = set()
    for row in confirm_rows:
        ok, _ = check_confirmation(row)
        if ok and row[0] in valid_events:
            confirmed_ids.add(row[0])

    # Считаем сумму
    totals = {}  # (author, context) -> sum
    for eid in confirmed_ids:
        author, context, weight = valid_events[eid]
        key = (author, context)
        totals[key] = totals.get(key, 0.0) + weight

    if not totals:
        print("(no valid confirmed contributions)")
        return

    # Опционально фильтруем по контексту
    if args.context:
        totals = {k: v for k, v in totals.items() if k[1] == args.context}
        if not totals:
            print(f"(no valid confirmed contributions in {args.context})")
            return

    # Группируем по автору (или по контексту — реши сам, что показывать)
    by_author = {}
    for (author, _ctx), total in totals.items():
        by_author[author] = by_author.get(author, 0.0) + total

    header = f"Reputation{' in ' + args.context if args.context else ''}:"
    print(header)
    for author, total in sorted(by_author.items(), key=lambda x: -x[1]):
        short = author[:30] + "..." if len(author) > 30 else author
        print(f"  {short:35s}  {total}")


def main():
    parser = argparse.ArgumentParser(prog="cl", description="Contribution Ledger v0.1.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("keygen", help="create a new identity")
    p.add_argument("name")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_keygen)

    p = sub.add_parser("add-contribution", help="record a contribution")
    p.add_argument("name")
    p.add_argument("context")
    p.add_argument("action")
    p.add_argument("weight", type=float)
    p.add_argument("--note")
    p.set_defaults(func=cmd_add_contribution)

    p = sub.add_parser("confirm", help="confirm a contribution")
    p.add_argument("name")
    p.add_argument("contribution_id")
    p.set_defaults(func=cmd_confirm)

    p = sub.add_parser("list", help="list events")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("verify", help="verify all signatures")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("reputation", help="show reputation")
    p.add_argument("--context")
    p.set_defaults(func=cmd_reputation)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
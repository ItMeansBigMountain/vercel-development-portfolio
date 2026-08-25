from __future__ import annotations

import sqlite3


class AuthorizationError(PermissionError):
    """Raised when an authenticated principal does not own a requested resource."""


def require_vehicle_owner(connection: sqlite3.Connection, user_id: str, vehicle_id: str) -> None:
    row = connection.execute(
        "SELECT 1 FROM vehicles v JOIN garages g ON g.id=v.garage_id "
        "WHERE v.id=? AND v.deleted_at IS NULL AND g.user_id=? AND g.deleted_at IS NULL",
        (vehicle_id, user_id),
    ).fetchone()
    if not row:
        raise AuthorizationError("resource not found")


def require_garage_owner(connection: sqlite3.Connection, user_id: str, garage_id: str) -> None:
    row = connection.execute(
        "SELECT 1 FROM garages WHERE id=? AND user_id=? AND deleted_at IS NULL",
        (garage_id, user_id),
    ).fetchone()
    if not row:
        raise AuthorizationError("resource not found")


def require_record_owner(connection: sqlite3.Connection, user_id: str, record_id: str) -> None:
    row = connection.execute(
        "SELECT 1 FROM service_records r JOIN vehicles v ON v.id=r.vehicle_id "
        "JOIN garages g ON g.id=v.garage_id WHERE r.id=? AND r.deleted_at IS NULL "
        "AND v.deleted_at IS NULL AND g.user_id=? AND g.deleted_at IS NULL",
        (record_id, user_id),
    ).fetchone()
    if not row:
        raise AuthorizationError("resource not found")


def require_connection_owner(connection: sqlite3.Connection, user_id: str, connection_id: str) -> None:
    row = connection.execute(
        "SELECT 1 FROM connected_accounts WHERE id=? AND user_id=?",
        (connection_id, user_id),
    ).fetchone()
    if not row:
        raise AuthorizationError("resource not found")

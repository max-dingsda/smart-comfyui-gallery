from __future__ import annotations

from pathlib import Path
import sqlite3
import time


def get_db_connection(database_file: str) -> sqlite3.Connection:
    """Create a SQLite connection with the app's required pragmas."""
    Path(database_file).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_file, timeout=60)
    conn.row_factory = sqlite3.Row
    for pragma in (
        "PRAGMA journal_mode=WAL;",
        "PRAGMA synchronous=NORMAL;",
        "PRAGMA foreign_keys = ON;",
    ):
        try:
            conn.execute(pragma)
        except sqlite3.OperationalError:
            # Some Windows/Conda setups fail optional PRAGMAs even though the
            # connection itself is usable. Keep the connection alive and fall
            # back to SQLite defaults rather than breaking API requests.
            continue
    return conn


def fetch_file_info(database_file: str, file_id: str, column: str = "*"):
    with get_db_connection(database_file) as conn:
        row = conn.execute(f"SELECT {column} FROM files WHERE id = ?", (file_id,)).fetchone()
    if not row:
        return None
    return dict(row) if column == "*" else row[0]


def fetch_collections_snapshot(database_file: str) -> dict[str, list[dict]]:
    with get_db_connection(database_file) as conn:
        flags = conn.execute("SELECT * FROM collections WHERE type='system_flag' ORDER BY id").fetchall()
        albums = conn.execute("SELECT * FROM collections WHERE type='user_album' ORDER BY name").fetchall()
    return {
        "flags": [dict(row) for row in flags],
        "albums": [dict(row) for row in albums],
    }


def get_collections_table_exists(database_file: str) -> bool:
    with get_db_connection(database_file) as conn:
        table_check = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='collections'"
        ).fetchone()
    return bool(table_check)


def exhibition_collections_ready(database_file: str) -> bool:
    with get_db_connection(database_file) as conn:
        public_colls = conn.execute(
            "SELECT COUNT(*) FROM collections WHERE type='user_album' AND is_public=1"
        ).fetchone()[0]
    return public_colls > 0


def ensure_sg_models_schema(conn: sqlite3.Connection) -> None:
    required_model_columns = {
        "civitai_status": "TEXT DEFAULT 'unknown'",
        "civitai_error": "TEXT",
    }
    cursor_models = conn.execute("PRAGMA table_info(sg_models)")
    existing_model_columns = {row["name"] for row in cursor_models.fetchall()}
    for col_name, col_type in required_model_columns.items():
        if col_name not in existing_model_columns:
            conn.execute(f"ALTER TABLE sg_models ADD COLUMN {col_name} {col_type}")


def init_db(
    database_file: str,
    db_schema_version: int,
    colors,
    conn: sqlite3.Connection | None = None,
) -> None:
    """Initialize or migrate the SmartGallery database schema."""
    close_conn = False
    if conn is None:
        conn = get_db_connection(database_file)
        close_conn = True

    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                path TEXT NOT NULL UNIQUE,
                mtime REAL NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                duration TEXT,
                dimensions TEXT,
                has_workflow INTEGER,
                is_favorite INTEGER DEFAULT 0,
                size INTEGER DEFAULT 0,
                last_scanned REAL DEFAULT 0,
                workflow_files TEXT DEFAULT '',
                workflow_prompt TEXT DEFAULT '',
                ai_last_scanned REAL DEFAULT 0,
                ai_caption TEXT,
                ai_embedding BLOB,
                ai_error TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_search_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                query TEXT NOT NULL,
                limit_results INTEGER DEFAULT 100,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                file_id TEXT NOT NULL,
                score REAL NOT NULL,
                FOREIGN KEY (session_id) REFERENCES ai_search_queue(session_id)
            );
            """
        )

        conn.execute("CREATE INDEX IF NOT EXISTS idx_queue_status ON ai_search_queue(status);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_results_session ON ai_search_results(session_id);")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_indexing_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                file_id TEXT,
                status TEXT DEFAULT 'pending',
                force_index INTEGER DEFAULT 0,
                params TEXT DEFAULT '{}',
                created_at REAL,
                updated_at REAL,
                error_msg TEXT,
                UNIQUE(file_path) ON CONFLICT REPLACE
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ai_idx_status ON ai_indexing_queue(status);")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_watched_folders (
                path TEXT PRIMARY KEY,
                recursive INTEGER DEFAULT 0,
                added_at REAL
            );
            """
        )

        conn.execute("CREATE TABLE IF NOT EXISTS ai_metadata (key TEXT PRIMARY KEY, value TEXT, updated_at REAL)")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mounted_folders (
                path TEXT PRIMARY KEY,
                target_source TEXT,
                created_at REAL
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                color TEXT,
                is_public INTEGER DEFAULT 0,
                created_at REAL
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS collection_files (
                collection_id INTEGER,
                file_id TEXT,
                added_at REAL,
                PRIMARY KEY (collection_id, file_id),
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS file_ratings (
                file_id TEXT,
                client_uuid TEXT,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                created_at REAL,
                PRIMARY KEY (file_id, client_uuid),
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS file_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT,
                client_uuid TEXT,
                author_name TEXT,
                comment_text TEXT,
                target_audience TEXT DEFAULT 'public',
                created_at REAL,
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
            );
            """
        )

        system_flags = [
            ("Approved", "system_flag", "#28a745"),
            ("Review", "system_flag", "#ffc107"),
            ("To Edit", "system_flag", "#17a2b8"),
            ("Rejected", "system_flag", "#dc3545"),
            ("Select", "system_flag", "#6f42c1"),
        ]

        existing_cols = conn.execute("SELECT COUNT(*) FROM collections WHERE type='system_flag'").fetchone()[0]
        if existing_cols == 0:
            print(f"{colors.BLUE}INFO: Initializing standard workflow tags...{colors.RESET}")
            conn.executemany(
                "INSERT INTO collections (name, type, color, is_public, created_at) VALUES (?, ?, ?, 0, ?)",
                [(name, coll_type, color, time.time()) for name, coll_type, color in system_flags],
            )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                phone_number TEXT,
                role TEXT CHECK(role IN ('USER', 'STAFF', 'MANAGER', 'CUSTOMER', 'FRIEND', 'GUEST', 'ADMIN')) DEFAULT 'GUEST',
                start_date DATE DEFAULT CURRENT_DATE,
                expiry_date DATE,
                is_active BOOLEAN DEFAULT 1
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sg_models (
                id TEXT PRIMARY KEY,
                section TEXT NOT NULL,
                source_folder TEXT NOT NULL,
                name TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                relative_path TEXT NOT NULL,
                size INTEGER NOT NULL,
                mtime INTEGER NOT NULL,
                scanned_at INTEGER NOT NULL,
                trigger_local TEXT,
                tags_local TEXT,
                architecture_local TEXT,
                sha256 TEXT,
                civitai_checked_at INTEGER,
                civitai_model_url TEXT,
                civitai_name TEXT,
                civitai_version_name TEXT,
                civitai_type TEXT,
                civitai_base_model TEXT,
                civitai_creator TEXT,
                civitai_license TEXT,
                civitai_trigger TEXT,
                civitai_tags TEXT,
                civitai_status TEXT DEFAULT 'unknown',
                civitai_error TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sg_models_section ON sg_models(section);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sg_models_name ON sg_models(name);")

        required_file_columns = {
            "size": "INTEGER DEFAULT 0",
            "last_scanned": "REAL DEFAULT 0",
            "workflow_files": "TEXT DEFAULT ''",
            "workflow_prompt": "TEXT DEFAULT ''",
            "ai_last_scanned": "REAL DEFAULT 0",
            "ai_caption": "TEXT",
            "ai_embedding": "BLOB",
            "ai_error": "TEXT",
        }

        try:
            cursor_fc = conn.execute("PRAGMA table_info(file_comments)")
            fc_columns = {row["name"] for row in cursor_fc.fetchall()}
            if "target_audience" not in fc_columns:
                print("INFO: Updating Database Schema... Adding 'target_audience' to file_comments")
                conn.execute("ALTER TABLE file_comments ADD COLUMN target_audience TEXT DEFAULT 'public'")
        except Exception as exc:
            print(f"WARNING: Could not migrate file_comments table: {exc}")

        try:
            cursor_col = conn.execute("PRAGMA table_info(collections)")
            col_columns = {row["name"] for row in cursor_col.fetchall()}
            if "is_public" not in col_columns:
                print("INFO: Updating Database Schema... Adding 'is_public' to collections")
                conn.execute("ALTER TABLE collections ADD COLUMN is_public INTEGER DEFAULT 0")
        except Exception as exc:
            print(f"WARNING: Could not migrate collections table: {exc}")

        cursor = conn.execute("PRAGMA table_info(files)")
        existing_columns = {row["name"] for row in cursor.fetchall()}

        for col_name, col_type in required_file_columns.items():
            if col_name not in existing_columns:
                print(f"INFO: Updating Database Schema... Adding missing column '{col_name}'")
                try:
                    conn.execute(f"ALTER TABLE files ADD COLUMN {col_name} {col_type}")
                except Exception as exc:
                    print(f"WARNING: Could not add column {col_name}: {exc}")

        try:
            ensure_sg_models_schema(conn)
        except Exception as exc:
            print(f"WARNING: Could not migrate sg_models table: {exc}")

        try:
            cur = conn.execute("PRAGMA user_version")
            current_ver = cur.fetchone()[0]
            if current_ver != db_schema_version:
                print(f"INFO: Updating Database Schema Version: {current_ver} -> {db_schema_version}")
                conn.execute(f"PRAGMA user_version = {db_schema_version}")
        except Exception as exc:
            print(f"WARNING: Could not update DB schema version: {exc}")

        conn.commit()

    except Exception as exc:
        print(f"CRITICAL DATABASE ERROR: {exc}")

    finally:
        if close_conn:
            conn.close()

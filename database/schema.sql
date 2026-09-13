
-- NOVEL OS SQLITE SCHEMA FOR PHA_TROI

CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- character, faction, location, artifact, concept
    aliases TEXT, -- JSON array
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS canon_entries (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL, -- premise, cosmology, cultivation, rule, character
    key TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    level TEXT NOT NULL, -- LOCKED, CONFIRMED, PROVISIONAL, UNKNOWN, FORBIDDEN_ASSUMPTION, PROPOSED
    approved_by TEXT DEFAULT 'Author',
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id TEXT NOT NULL,
    chapter_num INTEGER NOT NULL,
    location_id TEXT,
    cultivation_realm TEXT,
    physical_condition TEXT,
    injuries_json TEXT,
    inventory_json TEXT,
    emotional_state TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(character_id) REFERENCES entities(id)
);

CREATE TABLE IF NOT EXISTS knowledge_matrix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_key TEXT NOT NULL,
    statement TEXT NOT NULL,
    character_id TEXT NOT NULL,
    epistemic_status TEXT NOT NULL, -- KNOWN, SUSPECTED, BELIEVED, MISUNDERSTOOD, FALSE_BELIEF, UNKNOWN, FORGOTTEN
    chapter_num INTEGER NOT NULL,
    source_event_id TEXT
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    chapter_num INTEGER,
    scene_num INTEGER,
    absolute_time TEXT,
    relative_order INTEGER,
    location_id TEXT,
    participants_json TEXT,
    summary TEXT,
    outcome TEXT
);

CREATE TABLE IF NOT EXISTS world_nodes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT,
    cosmology_rank INTEGER NOT NULL, -- 1=??i ??i Gi?i, 2=V?c, 3=Tinh H?i, 4=V? Di?n, 5=Th? Gi?i, 6=Tr?i ??t
    cultivation_system TEXT,
    status TEXT DEFAULT 'ACTIVE',
    access_conditions TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS world_edges (
    id TEXT PRIMARY KEY,
    source_node_id TEXT NOT NULL,
    target_node_id TEXT NOT NULL,
    connection_type TEXT NOT NULL, -- route, portal, barrier, seal, forbidden
    travel_time_hours REAL DEFAULT 0,
    access_requirement TEXT,
    FOREIGN KEY(source_node_id) REFERENCES world_nodes(id),
    FOREIGN KEY(target_node_id) REFERENCES world_nodes(id)
);

CREATE TABLE IF NOT EXISTS foreshadowing_ledger (
    id TEXT PRIMARY KEY,
    seed_description TEXT NOT NULL,
    planted_chapter INTEGER NOT NULL,
    planted_scene INTEGER,
    notices_json TEXT,
    actual_meaning TEXT,
    payoff_chapter INTEGER,
    payoff_scene INTEGER,
    status TEXT NOT NULL, -- PLANTED, ACTIVE, PARTIALLY_PAID, PAID, ABANDONED, REDIRECTED, RED_HERRING
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plot_nodes (
    id TEXT PRIMARY KEY,
    node_type TEXT NOT NULL, -- volume, arc, chapter, scene
    parent_id TEXT,
    order_index INTEGER NOT NULL,
    title TEXT NOT NULL,
    objective TEXT,
    conflict TEXT,
    stakes TEXT,
    pov TEXT,
    status TEXT DEFAULT 'PLANNED', -- PLANNED, DRAFTING, REVISING, CANONIZED
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    why_it_matters TEXT,
    affected_canon TEXT,
    affected_characters TEXT,
    affected_plot TEXT,
    alternatives_json TEXT,
    recommended_option TEXT,
    risk TEXT,
    status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, SUPERSEDED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS continuity_errors (
    id TEXT PRIMARY KEY,
    chapter_num INTEGER,
    severity TEXT NOT NULL, -- LOW, MEDIUM, HIGH, CRITICAL
    category TEXT NOT NULL, -- CANON, CHARACTER, POV, TIMELINE, LOCATION, POWER, RELATIONSHIP, FORESHADOWING, STYLE, NARRATIVE, RESEARCH
    description TEXT NOT NULL,
    conflicting_facts_json TEXT,
    possible_fixes_json TEXT,
    status TEXT DEFAULT 'ACTIVE', -- ACTIVE, RESOLVED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_type TEXT NOT NULL,
    description TEXT NOT NULL,
    author TEXT DEFAULT 'NovelOS',
    details_json TEXT
);

-- Full-text search for fast context retrieval across thousands of chapters
CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
    doc_id UNINDEXED,
    doc_type, -- chapter, bible, lore, event
    title,
    content,
    tags
);

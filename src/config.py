"""
config.py — App-wide constants: topics, difficulties, and UI copy.
Add new topics here; no other file needs changing.
"""

# ── Interview topics ──────────────────────────────────────────────────────────
TOPICS: dict[str, dict] = {
    "Python": {
        "icon": "🐍",
        "description": "Core language features, data structures, OOP, and standard library.",
        "tags": ["variables", "loops", "functions", "classes", "modules", "async"],
    },
    "SQL": {
        "icon": "🗄️",
        "description": "Queries, joins, aggregations, indexing, and database design.",
        "tags": ["SELECT", "JOIN", "GROUP BY", "indexes", "transactions", "normalization"],
    },
    "OOP": {
        "icon": "🧩",
        "description": "Principles of object-oriented design: SOLID, patterns, inheritance.",
        "tags": ["encapsulation", "inheritance", "polymorphism", "abstraction", "SOLID"],
    },
    "Data Structures": {
        "icon": "🌳",
        "description": "Arrays, linked lists, trees, graphs, heaps, and hash maps.",
        "tags": ["arrays", "stacks", "queues", "trees", "graphs", "hashing"],
    },
    "Machine Learning": {
        "icon": "🤖",
        "description": "Algorithms, model evaluation, feature engineering, and deployment.",
        "tags": ["regression", "classification", "overfitting", "cross-validation", "ensembles"],
    },
    "System Design": {
        "icon": "🏗️",
        "description": "Scalability, microservices, caching, load balancing, and databases at scale.",
        "tags": ["CAP theorem", "sharding", "caching", "message queues", "API design"],
    },
    "JavaScript": {
        "icon": "⚡",
        "description": "ES6+, async/await, closures, the event loop, and DOM.",
        "tags": ["closures", "promises", "event loop", "prototype", "modules"],
    },
    "Django / Flask": {
        "icon": "🌐",
        "description": "Web frameworks, REST APIs, ORM, authentication, and middleware.",
        "tags": ["routing", "ORM", "views", "serializers", "authentication", "middleware"],
    },
}

# ── Difficulty levels ─────────────────────────────────────────────────────────
DIFFICULTIES: list[str] = ["Easy", "Medium", "Hard"]

DIFFICULTY_META: dict[str, dict] = {
    "Easy":   {"color": "#1D9E75", "icon": "🟢", "desc": "Definitions & basic concepts"},
    "Medium": {"color": "#BA7517", "icon": "🟡", "desc": "Scenario-based & applied questions"},
    "Hard":   {"color": "#E24B4A", "icon": "🔴", "desc": "Deep dives & system design"},
}

# ── Score thresholds for verdict colours ─────────────────────────────────────
SCORE_COLOURS: dict[str, str] = {
    "Excellent":        "#1D9E75",
    "Good":             "#378ADD",
    "Average":          "#BA7517",
    "Needs Improvement":"#E24B4A",
    "Poor":             "#A32D2D",
}

# ── App metadata ─────────────────────────────────────────────────────────────
APP_TITLE   = "AI Interview Prep Assistant"
APP_TAGLINE = "Generate real interview questions · Get AI-powered feedback · Ace your next interview"
APP_VERSION = "1.0.0"

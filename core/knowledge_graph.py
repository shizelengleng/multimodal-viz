from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ConceptCategory(str, Enum):
    DEFINITION = "definition"
    PRINCIPLE = "principle"
    EXAMPLE = "example"
    APPLICATION = "application"
    THEORY = "theory"
    PERSON = "person"
    EVENT = "event"
    PROCESS = "process"
    OTHER = "other"


class RelationType(str, Enum):
    INFLUENCES = "influences"
    PREREQUISITE_OF = "prerequisite_of"
    PART_OF = "part_of"
    CONTRASTS_WITH = "contrasts_with"
    EXAMPLE_OF = "example_of"
    LEADS_TO = "leads_to"
    RELATES_TO = "relates_to"


VALID_CATEGORIES = {c.value for c in ConceptCategory}


class Concept(BaseModel):
    id: str
    name: str
    description: str = ""
    category: str = "other"  # any string, mapped to known category or "other"
    difficulty: str = "basic"  # basic | intermediate | advanced

    @field_validator("id")
    @classmethod
    def id_format(cls, v: str) -> str:
        if not v.startswith("c"):
            return f"c{v}"
        return v

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        if v in VALID_CATEGORIES:
            return v
        return "other"


class Relation(BaseModel):
    source: str
    target: str
    type: RelationType = RelationType.RELATES_TO
    label: str = ""

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, v):
        try:
            return RelationType(v)
        except ValueError:
            return RelationType.RELATES_TO

    @field_validator("source", "target")
    @classmethod
    def id_format(cls, v: str) -> str:
        if not v.startswith("c"):
            return f"c{v}"
        return v


class KnowledgeGraph(BaseModel):
    title: str = "Knowledge Graph"
    source: str = "text"  # text | pdf
    layout_hint: str = "force_directed"  # force_directed | radial | hierarchical | timeline
    concepts: list[Concept] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)

    def validate_ids(self) -> list[str]:
        """Check all relations reference existing concepts. Returns list of errors."""
        concept_ids = {c.id for c in self.concepts}
        errors = []
        for i, r in enumerate(self.relations):
            if r.source not in concept_ids:
                errors.append(f"relation[{i}]: source '{r.source}' not found in concepts")
            if r.target not in concept_ids:
                errors.append(f"relation[{i}]: target '{r.target}' not found in concepts")
        return errors

    def to_json(self, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, data: str | dict) -> "KnowledgeGraph":
        if isinstance(data, str):
            data = json.loads(data)
        return cls(**data)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "KnowledgeGraph":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))


def auto_detect_layout(graph: KnowledgeGraph) -> str:
    """Auto-detect best layout based on relationship patterns."""
    if not graph.relations:
        return "radial"

    relation_types = {r.type for r in graph.relations}
    has_hierarchy = RelationType.PART_OF in relation_types
    has_sequence = (
        RelationType.LEADS_TO in relation_types
        or RelationType.PREREQUISITE_OF in relation_types
    )

    if has_sequence and len(graph.relations) <= len(graph.concepts) * 1.2:
        return "hierarchical"
    if has_hierarchy and len(graph.concepts) > 5:
        return "radial"
    return "force_directed"

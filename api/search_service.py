"""Search service backed by generated index artifacts."""

from __future__ import annotations

import json
import re
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .config import SEARCH_INDEX_JS_PATH, SEARCH_INDEX_JSON_PATH
from .models import SearchRequest, SearchResult


class SearchService:
    """Load index data and execute filtered search queries."""

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []
        self._signature: Tuple[Tuple[str, int, int], ...] = tuple()
        self._lock = Lock()

    def get_index_count(self) -> int:
        """Return cached index record count."""
        self._refresh_if_needed()
        return len(self._records)

    def search(self, request: SearchRequest) -> Tuple[int, List[SearchResult]]:
        """Execute search against cached index records."""
        self._refresh_if_needed()
        filtered = [
            item for item in self._records if self._matches(item, request)
        ]
        self._sort(filtered, request.sortBy)

        total = len(filtered)
        end_offset = request.offset + request.limit
        paged = filtered[request.offset:end_offset]
        results = [SearchResult(**item) for item in paged]
        return total, results

    def _refresh_if_needed(self) -> None:
        signature = self._compute_signature()
        with self._lock:
            if signature == self._signature and self._records:
                return
            self._records = self._load_records()
            self._signature = signature

    def _compute_signature(self) -> Tuple[Tuple[str, int, int], ...]:
        signatures: List[Tuple[str, int, int]] = []
        for path in (SEARCH_INDEX_JS_PATH, SEARCH_INDEX_JSON_PATH):
            if path.exists():
                stat = path.stat()
                signatures.append((str(path), stat.st_mtime_ns, stat.st_size))
        return tuple(signatures)

    def _load_records(self) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        if SEARCH_INDEX_JS_PATH.exists():
            js_content = SEARCH_INDEX_JS_PATH.read_text(encoding="utf-8")
            js_records = self._load_js_records(js_content)
            if js_records:
                records.extend(js_records)

        if SEARCH_INDEX_JSON_PATH.exists() and not records:
            json_content = SEARCH_INDEX_JSON_PATH.read_text(encoding="utf-8")
            payload = json.loads(json_content)
            records.extend(self._load_json_records(payload))

        return [self._normalize(record) for record in records]

    def _load_json_records(
        self,
        payload: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []

        documents = payload.get("documents", [])
        if isinstance(documents, list):
            records.extend(
                [record for record in documents if isinstance(record, dict)]
            )

        characters = payload.get("characters", [])
        if isinstance(characters, list):
            for character in characters:
                if not isinstance(character, dict):
                    continue
                records.append(
                    {
                        "id": character.get("id"),
                        "title": character.get("name"),
                        "type": "Character Profile",
                        "content": character.get("summary")
                        or character.get("searchable_text"),
                        "location": character.get("location")
                        or "Unknown",
                        "source": "Character Directory",
                        "person": character.get("name"),
                        "tags": (
                            [character.get("role")]
                            if character.get("role")
                            else []
                        ),
                    }
                )

        locations = payload.get("locations", [])
        if isinstance(locations, list):
            for location in locations:
                if not isinstance(location, dict):
                    continue
                records.append(
                    {
                        "id": location.get("id"),
                        "title": location.get("name"),
                        "type": "Location Record",
                        "location": location.get("country") or "Unknown",
                        "content": location.get("type"),
                        "source": "Location Directory",
                        "tags": (
                            [location.get("type")]
                            if location.get("type")
                            else []
                        ),
                    }
                )

        events = payload.get("events", [])
        if isinstance(events, list):
            for event in events:
                if not isinstance(event, dict):
                    continue
                records.append(
                    {
                        "id": (
                            f"event-{event.get('date', '')}-"
                            f"{event.get('title', '')}"
                        ),
                        "title": event.get("title"),
                        "type": "Timeline Event",
                        "date": event.get("date") or "",
                        "content": event.get("description"),
                        "source": "Timeline",
                    }
                )

        return records

    def _load_js_records(self, js_content: str) -> List[Dict[str, Any]]:
        pattern = r"const\s+SEARCH_DATA\s*=\s*(\[[\s\S]*?\]);"
        match = re.search(pattern, js_content)
        if match:
            try:
                parsed = json.loads(match.group(1))
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                return []

        index_pattern = r"const\s+SEARCH_INDEX\s*=\s*(\{[\s\S]*?\});"
        index_match = re.search(index_pattern, js_content)
        if not index_match:
            return []

        try:
            index_payload = json.loads(index_match.group(1))
        except json.JSONDecodeError:
            return []

        documents = index_payload.get("documents", [])
        if not isinstance(documents, list):
            return []
        return [record for record in documents if isinstance(record, dict)]

    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        text_blob = self._extract_text_blob(raw)
        tags = self._extract_tags(raw)
        relevance_score = self._coerce_relevance(raw.get("relevance", 70))
        case_number_raw = raw.get("case_number") or raw.get("caseNumber")
        resolved_type = self._resolve_type(raw)
        resolved_title = self._resolve_text(
            raw,
            ("title", "name"),
            "Untitled Record",
        )
        resolved_location = self._resolve_text(
            raw,
            ("location", "country"),
            "Unknown",
        )
        resolved_source = self._resolve_text(
            raw,
            ("source",),
            "Public Records",
        )
        resolved_person = self._resolve_text(raw, ("person",), "")

        return {
            "id": self._resolve_text(raw, ("id", "name"), "unknown"),
            "title": resolved_title,
            "type": resolved_type,
            "date": str(raw.get("date") or ""),
            "location": resolved_location,
            "redaction": self._resolve_text(
                raw,
                ("redaction_status", "redaction"),
                "Unknown",
            ),
            "snippet": self._build_snippet(text_blob),
            "tags": tags,
            "relevance": relevance_score,
            "source": resolved_source,
            "caseNumber": self._normalize_case_number(case_number_raw),
            "person": resolved_person,
            "_search_blob": self._build_search_blob(
                title=resolved_title,
                text_blob=text_blob,
                tags=tags,
                person=resolved_person,
                location=resolved_location,
                record_type=resolved_type,
                source=resolved_source,
            ),
        }

    def _resolve_type(self, raw: Dict[str, Any]) -> str:
        explicit_type = self._resolve_text(
            raw,
            ("type", "category"),
            "",
        ).strip()

        signal_fields = [
            raw.get("id"),
            raw.get("name"),
            raw.get("title"),
            raw.get("path"),
            raw.get("summary"),
            raw.get("searchable_text"),
            raw.get("content"),
        ]
        signal_blob = " ".join(
            str(value or "") for value in signal_fields
        ).lower()

        if any(
            term in signal_blob
            for term in ("flight", "manifest", "passenger")
        ):
            return "Flight Log"

        if explicit_type.startswith("."):
            return "Document"

        if explicit_type and explicit_type.lower() not in {
            "document",
            "general document",
        }:
            return explicit_type

        return "Document"

    def _normalize_case_number(self, value: Any) -> Optional[str]:
        if value in (None, "", "N/A"):
            return None
        return str(value)

    def _resolve_text(
        self,
        raw: Dict[str, Any],
        keys: Sequence[str],
        default: str,
    ) -> str:
        for key in keys:
            value = raw.get(key)
            if value is not None and value != "":
                return str(value)
        return default

    def _extract_text_blob(self, raw: Dict[str, Any]) -> str:
        candidates = ["content", "summary", "searchable_text"]
        for key in candidates:
            value = raw.get(key)
            if value:
                return str(value)
        return ""

    def _extract_tags(self, raw: Dict[str, Any]) -> List[str]:
        tags = raw.get("tags")
        if not isinstance(tags, list):
            return []
        return [str(tag) for tag in tags]

    def _coerce_relevance(self, value: Any) -> int:
        try:
            return max(0, min(100, int(value)))
        except (TypeError, ValueError):
            return 70

    def _build_snippet(self, text_blob: str) -> str:
        return text_blob[:320] + ("..." if len(text_blob) > 320 else "")

    def _build_search_blob(
        self,
        title: str,
        text_blob: str,
        tags: Sequence[str],
        person: str,
        location: str,
        record_type: str,
        source: str,
    ) -> str:
        sections = [
            title,
            text_blob,
            " ".join(tags),
            person,
            location,
            record_type,
            source,
        ]
        return " ".join(sections).lower()

    def _matches(self, item: Dict[str, Any], request: SearchRequest) -> bool:
        checks = (
            self._match_keyword(item, request.keyword),
            self._match_document_type(item, request.documentType),
            self._match_date_range(item, request.dateFrom, request.dateTo),
            self._match_location(item, request.location),
            self._match_location_keyword(item, request.locationKeyword),
            self._match_redaction(item, request.redactionStatus),
            self._match_person(item, request.person),
            self._match_case_number(item, request.caseNumber),
            self._match_source(item, request.fileSource),
            self._match_relevance(item, request.relevanceScore),
            self._match_flags(item, request.contentFlags),
        )
        return all(checks)

    def _match_keyword(self, item: Dict[str, Any], keyword: str) -> bool:
        if not keyword:
            return True
        return keyword.lower() in item["_search_blob"]

    def _match_document_type(
        self,
        item: Dict[str, Any],
        document_type: str,
    ) -> bool:
        if not document_type:
            return True
        expected_type = self._slugify(document_type)
        actual_type = self._slugify(item["type"])
        return expected_type == actual_type

    def _match_date_range(
        self,
        item: Dict[str, Any],
        date_from: str,
        date_to: str,
    ) -> bool:
        record_date = item["date"]
        if date_from and record_date and record_date < date_from:
            return False
        if date_to and record_date and record_date > date_to:
            return False
        return True

    def _match_location(self, item: Dict[str, Any], location: str) -> bool:
        if not location:
            return True
        expected_location = self._slugify(location)
        actual_location = self._slugify(item["location"])
        return expected_location in actual_location

    def _match_location_keyword(
        self,
        item: Dict[str, Any],
        location_keyword: str,
    ) -> bool:
        if not location_keyword:
            return True
        location_text = item["location"].lower()
        return location_keyword.lower() in location_text

    def _match_redaction(
        self,
        item: Dict[str, Any],
        statuses: Sequence[str],
    ) -> bool:
        if not statuses:
            return True
        expected_statuses = {self._slugify(status) for status in statuses}
        actual_status = self._slugify(item["redaction"])
        return any(expected in actual_status for expected in expected_statuses)

    def _match_person(self, item: Dict[str, Any], person: str) -> bool:
        if not person:
            return True
        person_blob = f"{item.get('person', '')} {item['snippet']}".lower()
        return person.lower() in person_blob

    def _match_case_number(
        self,
        item: Dict[str, Any],
        case_number: str,
    ) -> bool:
        if not case_number:
            return True
        item_case_number = (item.get("caseNumber") or "").lower()
        return case_number.lower() in item_case_number

    def _match_source(self, item: Dict[str, Any], source: str) -> bool:
        if not source:
            return True
        expected_source = self._slugify(source)
        actual_source = self._slugify(item["source"])
        return expected_source == actual_source

    def _match_relevance(
        self,
        item: Dict[str, Any],
        min_relevance: int,
    ) -> bool:
        if not min_relevance:
            return True
        return item["relevance"] >= min_relevance

    def _match_flags(
        self,
        item: Dict[str, Any],
        flags: Sequence[str],
    ) -> bool:
        if not flags:
            return True
        return self._matches_content_flags(item, flags)

    def _matches_content_flags(
        self,
        item: Dict[str, Any],
        flags: Sequence[str],
    ) -> bool:
        flag_terms = {
            "victim-mention": ["victim"],
            "financial-transaction": [
                "financial",
                "transaction",
                "bank",
                "wire",
            ],
            "travel-record": ["travel", "flight", "manifest", "passenger"],
            "property-mention": [
                "property",
                "estate",
                "island",
                "townhouse",
                "ranch",
            ],
            "associate-mention": [
                "associate",
                "contact",
                "address",
                "assistant",
            ],
            "evidence": ["evidence", "testimony", "deposition", "court"],
        }

        tags_text = " ".join(item["tags"])
        searchable = f"{item['title']} {item['snippet']} {tags_text}".lower()

        for flag in flags:
            terms = flag_terms.get(flag, [flag.replace("-", " ")])
            if not any(term in searchable for term in terms):
                return False
        return True

    def _sort(self, records: List[Dict[str, Any]], sort_by: str) -> None:
        if sort_by == "date-desc":
            records.sort(
                key=lambda row: self._safe_date(row.get("date")),
                reverse=True,
            )
        elif sort_by == "date-asc":
            records.sort(key=lambda row: self._safe_date(row.get("date")))
        elif sort_by == "type":
            records.sort(key=lambda row: row.get("type", "").lower())
        elif sort_by == "location":
            records.sort(key=lambda row: row.get("location", "").lower())
        else:
            records.sort(key=lambda row: row.get("relevance", 0), reverse=True)

    def _safe_date(self, value: Optional[str]) -> datetime:
        if not value:
            return datetime.min
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.min

    def _slugify(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


search_service = SearchService()

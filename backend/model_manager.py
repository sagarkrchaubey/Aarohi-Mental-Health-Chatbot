from __future__ import annotations

import time
from dataclasses import dataclass

from backend.config import DEFAULT_MODEL, FALLBACK_MODEL, MODEL_CACHE_TTL_SECONDS


@dataclass(frozen=True)
class ModelCatalogEntry:
    id: str
    label: str
    description: str
    status: str
    stable: bool = True


MODEL_CATALOG: dict[str, ModelCatalogEntry] = {
    "gemini-2.5-flash-lite": ModelCatalogEntry(
        id="gemini-2.5-flash-lite",
        label="Gemini 2.5 Flash Lite",
        description="Fastest, lightweight, ideal for quick support turns",
        status="stable",
    ),
    "gemini-2.5-flash": ModelCatalogEntry(
        id="gemini-2.5-flash",
        label="Gemini 2.5 Flash",
        description="Balanced speed and quality for most replies",
        status="stable",
    ),
    "gemini-2.5-pro": ModelCatalogEntry(
        id="gemini-2.5-pro",
        label="Gemini 2.5 Pro",
        description="Deep reasoning, slower, best for layered situations",
        status="stable",
    ),
    "gemini-2.0-flash": ModelCatalogEntry(
        id="gemini-2.0-flash",
        label="Gemini 2.0 Flash",
        description="Legacy model that may no longer be available",
        status="legacy",
        stable=False,
    ),
    "gemini-2.0-flash-001": ModelCatalogEntry(
        id="gemini-2.0-flash-001",
        label="Gemini 2.0 Flash 001",
        description="Legacy model that may no longer be available",
        status="legacy",
        stable=False,
    ),
    "gemini-2.0-flash-lite-001": ModelCatalogEntry(
        id="gemini-2.0-flash-lite-001",
        label="Gemini 2.0 Flash Lite 001",
        description="Legacy lightweight model that may no longer be available",
        status="legacy",
        stable=False,
    ),
    "gemini-2.0-flash-lite": ModelCatalogEntry(
        id="gemini-2.0-flash-lite",
        label="Gemini 2.0 Flash Lite",
        description="Legacy lightweight model that may no longer be available",
        status="legacy",
        stable=False,
    ),
}


@dataclass(frozen=True)
class ModelOption:
    id: str
    label: str
    description: str
    status: str


_model_cache = {
    "expires_at": 0.0,
    "model_ids": [],
}


def get_static_model_options() -> list[ModelOption]:
    stable_models = [
        MODEL_CATALOG["gemini-2.5-flash-lite"],
        MODEL_CATALOG["gemini-2.5-flash"],
        MODEL_CATALOG["gemini-2.5-pro"],
    ]
    return [
        ModelOption(
            id=entry.id,
            label=entry.label,
            description=entry.description,
            status=entry.status,
        )
        for entry in stable_models
    ]


def merge_model_options(dynamic_model_ids: list[str]) -> list[ModelOption]:
    visible_ids = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ]

    for model_id in dynamic_model_ids:
        entry = MODEL_CATALOG.get(model_id)
        if entry and not entry.stable and model_id not in visible_ids:
            visible_ids.append(model_id)

    return [
        ModelOption(
            id=MODEL_CATALOG[model_id].id,
            label=MODEL_CATALOG[model_id].label,
            description=MODEL_CATALOG[model_id].description,
            status=MODEL_CATALOG[model_id].status,
        )
        for model_id in visible_ids
        if model_id in MODEL_CATALOG
    ]


def cache_model_ids(model_ids: list[str]) -> None:
    _model_cache["model_ids"] = model_ids
    _model_cache["expires_at"] = time.time() + MODEL_CACHE_TTL_SECONDS


def get_cached_model_ids() -> list[str]:
    if time.time() < float(_model_cache["expires_at"]):
        return list(_model_cache["model_ids"])
    return []


def validate_model_selection(model_id: str, available_model_ids: list[str]) -> str:
    if model_id in available_model_ids:
        return model_id
    if model_id in MODEL_CATALOG and MODEL_CATALOG[model_id].stable:
        return model_id
    if DEFAULT_MODEL in available_model_ids or DEFAULT_MODEL in MODEL_CATALOG:
        return DEFAULT_MODEL
    return FALLBACK_MODEL

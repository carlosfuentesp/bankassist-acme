"""Normalize evidence returned by Genie into plain row dictionaries."""

from __future__ import annotations

from typing import Any


def _cell_value(cell: Any) -> Any:
    if not isinstance(cell, dict):
        return cell
    if "null_value" in cell:
        return None
    for key in (
        "string_value",
        "long_value",
        "double_value",
        "boolean_value",
        "decimal_value",
    ):
        if key in cell:
            return cell[key]
    return next(iter(cell.values()), None)


def extract_structured_rows(structured_response: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle known Genie attachment shapes without inventing absent fields."""

    content = structured_response.get("content") or {}
    attachments = content.get("queryAttachments") or content.get("query_attachments") or []
    rows: list[dict[str, Any]] = []

    for attachment in attachments:
        if not isinstance(attachment, dict):
            continue
        statement = attachment.get("statement_response") or {}
        result = (
            attachment.get("queryResult")
            or attachment.get("query_result")
            or statement.get("result")
            or attachment
        )
        data = result.get("data_array") or result.get("data") or result.get("rows") or []
        manifest = statement.get("manifest") or {}
        manifest_schema = manifest.get("schema") or {}
        columns = (
            result.get("columns")
            or result.get("schema")
            or manifest_schema.get("columns")
            or []
        )
        names = [
            str(column.get("name") if isinstance(column, dict) else column)
            for column in columns
        ]
        for item in data:
            if isinstance(item, dict) and "values" in item and names:
                values = [_cell_value(value) for value in item["values"]]
                rows.append(dict(zip(names, values, strict=False)))
            elif isinstance(item, dict):
                rows.append(item)
            elif isinstance(item, (list, tuple)) and names:
                rows.append(dict(zip(names, item, strict=False)))
    return rows

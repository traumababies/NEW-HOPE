"""Storage adapters.

Three container roles per the owner spec (The Library.txt, G):
  - Bunbuns   : permanent Library (originals + approved finals)
  - Ephemera  : scout quarantine (temporary, destroyed after Studio COMMIT)
  - Scrappa   : pipeline scratchpad (shared, transient working copies)

Delivery of heavy files is copy-first promotion + short-lived SAS tokens
("mirages"), never raw public links.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from ..config import settings


@dataclass(frozen=True)
class BlobRef:
    """A reference to a blob in one of the three role containers."""

    container: str
    key: str


def _service():
    # Lazy import so the app can boot without Azure credentials installed.
    from azure.storage.blob import BlobServiceClient

    if settings.azure_storage_connection_string:
        return BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)
    if settings.azure_blob_conn_str:
        return BlobServiceClient.from_connection_string(settings.azure_blob_conn_str)
    if settings.azure_storage_account_url:
        return BlobServiceClient(
            account_url=settings.azure_storage_account_url,
            credential=settings.azure_blob_key or None,
        )
    return BlobServiceClient(
        account_url=f"https://{settings.azure_blob_account}.blob.core.windows.net",
        credential=settings.azure_blob_key or None,
    )


def _ensure_container(service, container: str) -> None:
    try:
        service.create_container(container)
    except Exception:  # ContainerAlreadyExists
        pass


def put_blob(blob: BlobRef, data: bytes, content_type: str = "application/octet-stream") -> None:
    from azure.storage.blob import ContentSettings

    service = _service()
    _ensure_container(service, blob.container)
    service.get_blob_client(container=blob.container, blob=blob.key).upload_blob(
        data, overwrite=True, content_settings=ContentSettings(content_type=content_type)
    )


def get_blob(blob: BlobRef) -> bytes:
    service = _service()
    stream = service.get_blob_client(container=blob.container, blob=blob.key).download_blob()
    return stream.readall()


def delete_blob(blob: BlobRef) -> None:
    service = _service()
    service.get_blob_client(container=blob.container, blob=blob.key).delete_blob()


def exists(blob: BlobRef) -> bool:
    service = _service()
    return service.get_blob_client(container=blob.container, blob=blob.key).exists()


def mirage_url(blob: BlobRef, ttl_minutes: int = 60) -> str:
    """Short-lived read-only SAS URL ("mirage") for streaming to a browser."""
    from datetime import datetime, timedelta, timezone

    from azure.storage.blob import BlobSasPermissions, generate_blob_sas

    key = settings.azure_blob_key or _key_from_conn_str(settings.azure_storage_connection_string)
    account = settings.azure_blob_account
    if not key:
        # Fall back to a user-delegation-key SAS when only a connection string is known.
        from azure.storage.blob import BlobServiceClient

        service = _service()
        delegation_key = service.get_user_delegation_key(
            datetime.now(timezone.utc) - timedelta(minutes=5),
            datetime.now(timezone.utc) + timedelta(hours=1),
        )
        token = generate_blob_sas(
            account_name=service.account_name,
            container_name=blob.container,
            blob_name=blob.key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes),
            user_delegation_key=delegation_key,
        )
        account = service.account_name
    else:
        token = generate_blob_sas(
            account_name=account,
            account_key=key,
            container_name=blob.container,
            blob_name=blob.key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes),
        )
    return (
        f"https://{account}.blob.core.windows.net/"
        f"{blob.container}/{blob.key}?{token}"
    )


def _key_from_conn_str(conn_str: str) -> str:
    if not conn_str:
        return ""
    for part in conn_str.split(";"):
        if part.lower().startswith("accountkey="):
            return part.split("=", 1)[1]
    return ""


def copy_first_promotion(src: BlobRef, dst: BlobRef) -> None:
    """Copy src -> dst (copy-first), never move; caller deletes src to close the loop.

    Uses a client-side byte copy (download -> upload) so it works within one
    account without SAS-header pitfalls; the semantics are exactly copy-first
    (the source is never deleted here).
    """
    from azure.storage.blob import ContentSettings

    service = _service()
    _ensure_container(service, dst.container)
    src_client = service.get_blob_client(container=src.container, blob=src.key)
    props = src_client.get_blob_properties()
    stream = src_client.download_blob().readall()
    dst_client = service.get_blob_client(container=dst.container, blob=dst.key)
    dst_client.upload_blob(
        stream,
        overwrite=True,
        content_settings=ContentSettings(content_type=props.content_settings.content_type or "application/octet-stream"),
    )


def ensure_container(container: str) -> None:
    """Create a container if absent (idempotent)."""
    _ensure_container(_service(), container)


def enable_storage_cors(allowed_origins: list[str] | None = None) -> None:
    """Set account-level CORS so mirage SAS URLs render in the browser.

    Per The Library.txt G.8.b.iv: browser must be able to stream media from the
    central storage domain into the app pages without security blocks.
    """
    from azure.storage.blob import CorsRule

    service = _service()
    origins = allowed_origins or ["*"]
    service.set_service_properties(
        cors=[
            CorsRule(
                allowed_origins=origins,
                allowed_methods=["GET", "HEAD", "OPTIONS"],
                allowed_headers=["*"],
                exposed_headers=["content-type", "content-length"],
                max_age_in_seconds=3600,
            )
        ]
    )

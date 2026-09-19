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

    if settings.azure_blob_conn_str:
        return BlobServiceClient.from_connection_string(settings.azure_blob_conn_str)
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
    service = _service()
    _ensure_container(service, blob.container)
    service.get_blob_client(container=blob.container, blob=blob.key).upload_blob(
        data, overwrite=True, content_settings={"content_type": content_type}
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

    from azure.storage.blob import generate_blob_sas, BlobSasPermissions

    expiry = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    token = generate_blob_sas(
        account_name=settings.azure_blob_account,
        account_key=settings.azure_blob_key,
        container_name=blob.container,
        blob_name=blob.key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    return (
        f"https://{settings.azure_blob_account}.blob.core.windows.net/"
        f"{blob.container}/{blob.key}?{token}"
    )


def copy_first_promotion(src: BlobRef, dst: BlobRef) -> None:
    """Copy src -> dst (copy-first), never move; caller deletes src to close the loop."""
    service = _service()
    _ensure_container(service, dst.container)
    source_client = service.get_blob_client(container=src.container, blob=src.key)
    dest_client = service.get_blob_client(container=dst.container, blob=dst.key)
    dest_client.start_copy_from_url(source_client.url)

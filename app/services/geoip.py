"""MaxMind GeoLite2 lookup — optional when DB or license is configured."""

import logging
import tarfile
from io import BytesIO
from pathlib import Path

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_reader = None


def _download_geolite_country(db_path: Path) -> bool:
    if not settings.MAXMIND_LICENSE_KEY.strip():
        return False

    url = (
        "https://download.maxmind.com/app/geoip_download"
        f"?edition_id=GeoLite2-Country&license_key={settings.MAXMIND_LICENSE_KEY}&suffix=tar.gz"
    )
    try:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()

        db_path.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=BytesIO(resp.content), mode="r:gz") as tar:
            member = next(
                (m for m in tar.getmembers() if m.name.endswith(".mmdb")),
                None,
            )
            if not member:
                logger.warning("GeoLite2 archive has no .mmdb file")
                return False
            extracted = tar.extractfile(member)
            if not extracted:
                return False
            db_path.write_bytes(extracted.read())

        logger.info("GeoLite2-Country downloaded to %s", db_path)
        return True
    except Exception:
        logger.exception("MaxMind GeoLite2 download failed")
        return False


def init_geoip() -> None:
    global _reader
    if _reader is not None:
        return

    if not settings.maxmind_enabled:
        logger.debug("MaxMind GeoIP disabled (no DB path / license)")
        return

    try:
        from geoip2.database import Reader
    except ImportError:
        logger.warning("geoip2 package not installed")
        return

    db_path = settings.geoip_db_path_resolved
    if not db_path.is_file() and settings.MAXMIND_LICENSE_KEY.strip():
        _download_geolite_country(db_path)

    if not db_path.is_file():
        logger.warning("GeoIP database not found at %s", db_path)
        return

    _reader = Reader(str(db_path))
    logger.info("MaxMind GeoIP loaded: %s", db_path)


def lookup_ip(ip: str | None) -> dict[str, str | None]:
    """Return country_code (ISO), country_name — empty if lookup unavailable."""
    if not ip or not _reader:
        return {"country_code": None, "country_name": None, "city": None}

    try:
        from geoip2.errors import AddressNotFoundError

        record = _reader.country(ip)
        return {
            "country_code": record.country.iso_code,
            "country_name": record.country.name,
            "city": None,
        }
    except AddressNotFoundError:
        return {"country_code": None, "country_name": None, "city": None}
    except Exception:
        logger.exception("GeoIP lookup failed for %s", ip)
        return {"country_code": None, "country_name": None, "city": None}


def is_ksa(ip: str | None) -> bool:
    geo = lookup_ip(ip)
    return geo.get("country_code") == "SA"

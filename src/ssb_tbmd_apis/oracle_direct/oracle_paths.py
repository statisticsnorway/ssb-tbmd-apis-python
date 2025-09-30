from __future__ import annotations

from collections.abc import Iterable

from fagfunksjoner.prodsone.oradb import Oracle

Pair = tuple[str, str]


def _normalize_stamme_input(stamme_substamme: list[Pair] | Pair | str) -> list[Pair]:
    """Normalize the input into a list of (stamme, substamme) pairs.

    Accepts:
      - "$utd/nudb" or "utd/nudb" (string form; leading '$' allowed)
      - ("utd", "nudb") (tuple form)
      - [("utd", "nudb"), ("fob", "person")] (list of tuples)

    Raises:
      TypeError on malformed shapes or non-string elements.
    """
    if isinstance(stamme_substamme, str):
        parts = stamme_substamme.lstrip("$").split("/", 1)
        if len(parts) != 2:
            raise TypeError(
                "String form must be 'stamme/substamme' (optionally prefixed with '$')."
            )
        return [(parts[0], parts[1])]

    if isinstance(stamme_substamme, tuple):
        if len(stamme_substamme) != 2 or not all(
            isinstance(x, str) for x in stamme_substamme
        ):
            raise TypeError("Tuple form must be (stamme, substamme) of two strings.")
        return [(stamme_substamme[0].lstrip("$"), stamme_substamme[1])]

    # list of pairs
    if not isinstance(stamme_substamme, list) or not all(
        isinstance(t, tuple) for t in stamme_substamme
    ):
        raise TypeError("List form must be list of (stamme, substamme) tuples.")
    if not all(len(t) == 2 for t in stamme_substamme):
        raise TypeError(
            "Each tuple must have exactly two elements: (stamme, substamme)."
        )
    if not all(
        isinstance(t[0], str) and isinstance(t[1], str) for t in stamme_substamme
    ):
        raise TypeError("Each tuple must be two strings: (stamme, substamme).")
    return [(t[0].lstrip("$"), t[1]) for t in stamme_substamme]


def _build_single_query(stamme: str, substamme: str) -> str:
    """Build the SQL that yields full datadok paths for one (stamme, substamme)."""
    # NOTE: Keep exact structure/spacing to preserve behavior and tests.
    return f"""
            SELECT
                '${stamme.upper()}/{substamme}/arkiv/' || f.filklasse_navn || '/' || g.filnavn AS full_path
            FROM (
                SELECT filnivaa_id AS filklasse_id, filnivaa_navn AS filklasse_navn, filnivaa_filnivaa_id AS substamme_id
                FROM DATADOK.FILNIVAA
                WHERE filnivaa_nivaa = 'Filklasse'
                  AND filnivaa_filnivaa_id = (
                      SELECT filnivaa_id
                      FROM DATADOK.FILNIVAA
                      WHERE LOWER(filnivaa_navn) = LOWER('{substamme}')
                        AND filnivaa_nivaa = 'Substamme'
                        AND filnivaa_filnivaa_id = (
                            SELECT filnivaa_id
                            FROM DATADOK.FILNIVAA
                            WHERE LOWER(filnivaa_navn) = LOWER('{stamme}')
                              AND filnivaa_nivaa = 'Stamme'
                        )
                  )
            ) f
            JOIN (
                SELECT
                    filnivaa_navn,
                    CASE
                        WHEN filnivaa_datatype IS NOT NULL AND filnivaa_navn != filnivaa_datatype
                        THEN filnivaa_navn || filnivaa_datatype
                        ELSE filnivaa_navn
                    END AS filnavn,
                    filnivaa_filnivaa_id AS filklasse_id
                FROM DATADOK.FILNIVAA
                WHERE filnivaa_nivaa = 'Generasjon'
            ) g
            ON f.filklasse_id = g.filklasse_id
        """


def _build_union_query(pairs: Iterable[Pair]) -> str:
    """Combine per-pair queries with UNION ALL."""
    return " UNION ALL ".join(
        _build_single_query(stamme, substamme) for stamme, substamme in pairs
    )


def _execute_full_query(database: str, full_query: str) -> list[str]:
    """Execute query and stream results in batches, returning flattened paths."""
    results: list[str] = []
    with Oracle(db=database) as concur:
        concur.execute(full_query)
        while True:
            rows = concur.fetchmany(1000)
            if not rows:
                break
            results.extend(x[0] for x in rows)
    return results


def paths_in_substamme(
    stamme_substamme: list[Pair] | Pair | str,
    database: str,
) -> list[str]:
    """Try to recreate the paths used by Datadok under a stamme and substamme.

    Accepts:
      - "$stamme/substamme" or "stamme/substamme"
      - (stamme, substamme)
      - list of (stamme, substamme)

    Returns:
      list[str]: Full datadok paths (with a single leading '$').

    Raises:
      TypeError: On malformed input shapes or element types.
      OraError:  If the database operations fail.
    """
    pairs = _normalize_stamme_input(stamme_substamme)
    full_query = _build_union_query(pairs)
    return _execute_full_query(database, full_query)

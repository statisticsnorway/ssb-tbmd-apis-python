from fagfunksjoner.prodsone.oradb import Oracle
from oracledb import Error as OraError


def paths_in_substamme(
    stamme_substamme: list[tuple[str, ...]] | tuple[str, ...] | str, database: str
) -> list[str]:
    """Try to recreate the paths used by Datadok under a stamme and substamme.

    Requires that you have a user in the correct database, and that it has the datadok-read-role.
    The password for the database is also different from your usual password.

    Args:
        stamme_substamme: A single, or multiple linux-stammes you want to find paths in.
            Can be slash-seperated string, a tuple with two elements (stamme and substamme).
            Or it can be a list of tuples, where the tuples contain two string (stamme and substamme),
            allowing to get for many substammes at the same time (only enter database password once).
        database: The name of the database containing the datadok-data, and lots of other data at Statistics Norway.

    Returns:
        list[str]: The paths constructed from the contents in the database.

    Raises:
        TypeError: If the stamme_substamme parameter does not result in a list of tuples containing two strings.
        OraError: If the fetching from database doesnt work out.

    """
    # Normalize to list[tuple[str, str]]
    if isinstance(stamme_substamme, str):
        parts = stamme_substamme.lstrip("$").split("/")
        if len(parts) != 2:
            raise TypeError(
                "String form must be 'stamme/substamme' (optionally prefixed with '$')."
            )
        stamme_substamme_pairs: list[tuple[str, str]] = [(parts[0], parts[1])]
    elif isinstance(stamme_substamme, tuple):
        if len(stamme_substamme) != 2 or not all(
            isinstance(x, str) for x in stamme_substamme
        ):
            raise TypeError("Tuple form must be (stamme, substamme) of two strings.")
        stamme_substamme_pairs = [
            (stamme_substamme[0].lstrip("$"), stamme_substamme[1])
        ]
    else:
        if not isinstance(stamme_substamme, list) or not all(
            isinstance(t, tuple) for t in stamme_substamme
        ):
            raise TypeError("List form must be list of (stamme, substamme) tuples.")
        stamme_substamme_pairs = []
        for t in stamme_substamme:
            if len(t) != 2 or not all(isinstance(x, str) for x in t):
                raise TypeError("Each tuple must be two strings: (stamme, substamme).")
            stamme_substamme_pairs.append((t[0].lstrip("$"), t[1]))

    # Build queries with exactly one leading '$'
    union_queries: list[str] = []
    for stamme, substamme in stamme_substamme_pairs:
        union_queries.append(
            f"""
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
        )

    # Combine the individual queries with UNION ALL
    full_query = " UNION ALL ".join(union_queries)

    results = []
    try:
        with Oracle(db=database) as concur:
            concur.execute(full_query)
            # gets all the data in batches
            while True:
                rows = concur.fetchmany(1000)
                if not rows:
                    break
                else:
                    results += [x[0] for x in rows]
    except OraError as error:
        raise error
    return results

import getpass
import pandas as pd
from fagfunksjoner.prodsone.oradb import Oracle
from oracledb import Error as OraError


def paths_in_substamme(stamme_substamme: list[tuple[str, str]] | tuple[str, str] | str, database: str) -> list[str]:
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
        error: If the fetching from database doesnt work out.
    
    """
    # Support different informats by wrapping simple types in iterators
    if isinstance(stamme_substamme, str):
        stamme_substamme = tuple(stamme_substamme.split("/"))
    if isinstance(stamme_substamme, tuple):
        stamme_substamme_pairs = [stamme_substamme]
    else:
        stamme_substamme_pairs = stamme_substamme
    
    # Typecheck
    if not isinstance(stamme_substamme_pairs, list):
        raise TypeError("stamme_substamme_pairs must be a list.")
    if not all([isinstance(x, tuple) for x in stamme_substamme_pairs]):
        raise TypeError("Elements of stamme_substamme_pairs must be tuples.")
    if not all(isinstance(y, str) for x in stamme_substamme_pairs for y in x):
        raise TypeError("All element of the tuples in the list stamme_substamme_pairs must be strings.")
    
    
    union_queries = []
    for stamme, substamme in stamme_substamme_pairs:
        union_queries.append(f"""
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
        """)

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

import pandas as pd

def make_klass_df_codelist(codes: list[str|int],
                             names_bokmaal: list[str] | None = None,
                             names_nynorsk: list[str] | None = None,
                             names_engelsk: list[str] | None = None) -> pd.DataFrame:
    if names_bokmaal is None and names_nynorsk is None:
        raise ValueError("Must have content in names_bokmaal or names_nynorsk")
    for name in [names_bokmaal, names_nynorsk, names_engelsk]:
        if name and len(codes) != len(name):
            raise ValueError("Length of the entered names must match the length of codes.")
    
    cols = ["kode",
            "forelder",
            "navn_bokmål",
            "navn_nynorsk",
            "navn_engelsk",
            "kortnavn_bokmål",
            "kortnavn_nynorsk",
            "kortnavn_engelsk",
            "noter_bokmål",
            "noter_nynorsk",
            "noter_engelsk",
            "gyldig_fra",
            "gyldig_til",]
    
    data = {col: [None]*len(codes) for col in cols}
    data["kode"] = codes
    if names_bokmaal is not None:
        data["navn_bokmål"] = names_bokmaal
    if names_nynorsk is not None:
        data["navn_nynorsk"] = names_nynorsk
    if names_engelsk is not None:
        data["navn_engelsk"] = names_engelsk
        
    return pd.DataFrame({name: data for name, data in data.items()}) 

def make_klass_xml_codelist(path: str,
                            codes: list[str|int],
                            names_bokmaal: list[str] | None = None,
                            names_nynorsk: list[str] | None = None,
                            names_engelsk: list[str] | None = None) -> pd.DataFrame:
    df = make_klass_df_codelist(codes=codes,
                                names_bokmaal=names_bokmaal,
                                names_nynorsk=names_nynorsk,
                                names_engelsk=names_engelsk,)
    df.to_xml(path,
            root_name="versjon",
            row_name="element",
            namespaces={"ns1": "http://klass.ssb.no/version",},
            prefix="ns1")
    return df

#codelist = {
#    "1": "Utland",
#    "2": "Ikke utland",
#}

#make_klass_xml_codelist("carl_testfil.xml", codelist.keys(), codelist.values())

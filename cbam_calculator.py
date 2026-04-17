"""
Calculator simplu pentru greutate, emisii implicite si cost CBAM.

Valorile implicite de emisii din `valori_CBAM` sunt valorile furnizate
pentru codurile NC 7308 si 7210. Cheia `implicit` reprezinta valoarea
directa, iar cheia `2026` reprezinta valoarea cu mark-up.
"""

from __future__ import annotations

from dataclasses import dataclass


DENSITATE_OTEL_KG_M3 = 7850
GROSIME_TABLA_PANOU_EXTERIOR_IMPLICIT_MM = 0.5
GROSIME_TABLA_PANOU_INTERIOR_IMPLICIT_MM = 0.5
COEFICIENT_TABLA_EXTERIOR_PANOU = {
    "perete": 1.0,
    "acoperis": 1.08,
}


# Exemple kg/m2 pentru panouri sandwich, pe grosime totala panou.
greutate_panou: dict[int, float] = {
    40: 9.9,
    50: 10.3,
    60: 10.7,
    80: 11.5,
    100: 12.3,
    120: 13.1,
    150: 14.4,
}


# Valori implicite tCO2/t produs. Structura permite valori diferite pe an.
# Cheie: (tara_normalizata, cod_NC)
valori_CBAM: dict[tuple[str, str], dict[str, float]] = {
    ("default", "7308"): {"implicit": 4.1005, "2026": 4.51055},
    ("default", "7210"): {"implicit": 5.06385, "2026": 5.570235000000001},
    ("algeria", "7308"): {"implicit": 3.0, "2026": 3.3000000000000003},
    ("algeria", "7210"): {"implicit": 3.02, "2026": 3.3220000000000005},
    ("argentina", "7308"): {"implicit": 2.68, "2026": 2.9480000000000004},
    ("argentina", "7210"): {"implicit": 3.01, "2026": 3.311},
    ("australia", "7308"): {"implicit": 3.0, "2026": 3.3000000000000003},
    ("australia", "7210"): {"implicit": 3.2, "2026": 3.5200000000000005},
    ("azerbaijan", "7308"): {"implicit": 0.14, "2026": 0.15400000000000003},
    ("azerbaijan", "7210"): {"implicit": 1.89, "2026": 2.079},
    ("bosnia and herzegovina", "7308"): {"implicit": 2.29, "2026": 2.519},
    ("bosnia and herzegovina", "7210"): {"implicit": 2.85, "2026": 3.1350000000000002},
    ("brazil", "7308"): {"implicit": 1.73, "2026": 1.903},
    ("brazil", "7210"): {"implicit": 2.91, "2026": 3.2010000000000005},
    ("canada", "7308"): {"implicit": 1.51, "2026": 1.6610000000000003},
    ("canada", "7210"): {"implicit": 2.91, "2026": 3.2010000000000005},
    ("chile", "7308"): {"implicit": 2.05, "2026": 2.255},
    ("chile", "7210"): {"implicit": 2.54, "2026": 2.7940000000000005},
    ("china", "7308"): {"implicit": 3.205, "2026": 3.5255000000000005},
    ("china", "7210"): {"implicit": 6.035, "2026": 6.6385000000000005},
    ("colombia", "7308"): {"implicit": 2.89, "2026": 3.1790000000000003},
    ("colombia", "7210"): {"implicit": 3.58, "2026": 3.9380000000000006},
    ("india", "7308"): {"implicit": 4.28, "2026": 4.708000000000001},
    ("india", "7210"): {"implicit": 5.93, "2026": 6.523000000000001},
    ("indonesia", "7308"): {"implicit": 8.25, "2026": 9.075000000000001},
    ("indonesia", "7210"): {"implicit": 8.25, "2026": 9.075000000000001},
    ("iran", "7308"): {"implicit": 1.94, "2026": 2.134},
    ("iran", "7210"): {"implicit": 2.55, "2026": 2.805},
    ("japan", "7308"): {"implicit": 2.13, "2026": 2.343},
    ("japan", "7210"): {"implicit": 2.95, "2026": 3.2450000000000006},
    ("kazakhstan", "7308"): {"implicit": 5.36, "2026": 5.896000000000001},
    ("kazakhstan", "7210"): {"implicit": 5.36, "2026": 5.896000000000001},
    ("mexico", "7308"): {"implicit": 2.81, "2026": 3.091},
    ("mexico", "7210"): {"implicit": 2.99, "2026": 3.2890000000000006},
    ("myanmar", "7308"): {"implicit": 0.47, "2026": 0.517},
    ("myanmar", "7210"): {"implicit": 2.7, "2026": 2.9700000000000006},
    ("new zealand", "7308"): {"implicit": 2.43, "2026": 2.6730000000000005},
    ("new zealand", "7210"): {"implicit": 2.9, "2026": 3.19},
    ("north macedonia", "7308"): {"implicit": 1.53, "2026": 1.6830000000000003},
    ("north macedonia", "7210"): {"implicit": 2.69, "2026": 2.959},
    ("philippines", "7308"): {"implicit": 0.74, "2026": 0.8140000000000001},
    ("philippines", "7210"): {"implicit": 2.18, "2026": 2.3980000000000006},
    ("russia", "7308"): {"implicit": 3.59, "2026": 3.9490000000000003},
    ("russia", "7210"): {"implicit": 3.59, "2026": 3.9490000000000003},
    ("serbia", "7308"): {"implicit": 2.41, "2026": 2.6510000000000002},
    ("serbia", "7210"): {"implicit": 2.48, "2026": 2.728},
    ("south africa", "7308"): {"implicit": 4.22, "2026": 4.642},
    ("south africa", "7210"): {"implicit": 4.22, "2026": 4.642},
    ("south korea", "7308"): {"implicit": 2.144, "2026": 2.3584000000000005},
    ("south korea", "7210"): {"implicit": 3.864, "2026": 4.2504},
    ("taiwan", "7308"): {"implicit": 2.333, "2026": 2.5663000000000005},
    ("taiwan", "7210"): {"implicit": 2.423, "2026": 2.6653000000000002},
    ("thailand", "7308"): {"implicit": 2.330821429, "2026": 2.5639035719},
    ("thailand", "7210"): {"implicit": 4.2895, "2026": 4.718450000000001},
    ("turkiye", "7308"): {"implicit": 2.51, "2026": 2.761},
    ("turkiye", "7210"): {"implicit": 5.52, "2026": 6.072},
    ("ukraine", "7308"): {"implicit": 2.54352512, "2026": 2.797877632},
    ("ukraine", "7210"): {"implicit": 3.413, "2026": 3.7543},
    ("united kingdom", "7308"): {"implicit": 2.5, "2026": 2.75},
    ("united kingdom", "7210"): {"implicit": 3.04, "2026": 3.3440000000000003},
    ("united states", "7308"): {"implicit": 1.44, "2026": 1.584},
    ("united states", "7210"): {"implicit": 2.9, "2026": 3.19},
    ("uzbekistan", "7308"): {"implicit": 3.21, "2026": 3.531},
    ("uzbekistan", "7210"): {"implicit": 3.01, "2026": 3.311},
    ("vietnam", "7308"): {"implicit": 2.37, "2026": 2.607},
    ("vietnam", "7210"): {"implicit": 2.84, "2026": 3.124},
}


COD_NC_IMPLICIT_PE_PRODUS = {
    "panou_sandwich": "7308",
    "tabla_cutata": "7210",
    "profil_inalt": "7210",
}


# Tari terte uzuale pentru care CBAM poate fi relevant la import in UE.
# Sunt excluse statele membre UE si tarile din Anexa III CBAM:
# Islanda, Liechtenstein, Norvegia si Elvetia.
tari_cbam: list[str] = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo",
    "Costa Rica",
    "Cote d'Ivoire",
    "Cuba",
    "Democratic Republic of the Congo",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Gabon",
    "Gambia",
    "Georgia",
    "Ghana",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Israel",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Qatar",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkmenistan",
    "Tuvalu",
    "Turkiye",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]


@dataclass(frozen=True)
class RezultatCBAM:
    greutate_kg_m2: float
    greutate_tone: float
    emisii_tco2: float
    cost_cbam_eur: float
    cost_cbam_eur_m2: float
    valoare_implicita: float
    sursa_valoare_implicita: str


def normalizeaza_tara(tara: str) -> str:
    """Normalizeaza numele tarii pentru cautarea in dictionar."""
    tara_curata = tara.strip().lower()
    aliasuri = {
        "turkey": "turkiye",
        "türkiye": "turkiye",
        "turcia": "turkiye",
        "republic of turkiye": "turkiye",
        "china": "china",
        "cina": "china",
        "myanmar_burma": "myanmar",
        "myanmar/burma": "myanmar",
        "burma": "myanmar",
        "united states": "united states",
        "usa": "united states",
        "u.s.a.": "united states",
        "united states of america": "united states",
        "sua": "united states",
        "united kingdom": "united kingdom",
        "uk": "united kingdom",
        "great britain": "united kingdom",
        "marea britanie": "united kingdom",
    }
    return aliasuri.get(tara_curata, tara_curata)


def normalizeaza_tip_panou(tip_panou: str | None) -> str:
    tip = (tip_panou or "perete").strip().lower()
    aliasuri = {
        "wall": "perete",
        "panou_perete": "perete",
        "perete": "perete",
        "roof": "acoperis",
        "acoperis": "acoperis",
        "panou_acoperis": "acoperis",
    }
    tip_norm = aliasuri.get(tip, tip)
    if tip_norm not in COEFICIENT_TABLA_EXTERIOR_PANOU:
        raise ValueError("Tip panou invalid. Folositi: perete sau acoperis.")
    return tip_norm


def greutate_m2(grosime_mm: float, densitate_kg_m3: float = DENSITATE_OTEL_KG_M3) -> float:
    """
    Calculeaza greutatea pe m2 pentru o foaie de otel.

    Formula:
        grosime_m = grosime_mm / 1000
        kg_m2 = grosime_m * densitate_kg_m3
    """
    if grosime_mm <= 0:
        raise ValueError("Grosimea tablei trebuie sa fie mai mare decat 0.")

    return (grosime_mm / 1000) * densitate_kg_m3


def greutate_miez_panou_kg_m2(grosime_panou_mm: int) -> float:
    """
    Estimeaza greutatea miezului panoului din tabelul existent.

    Tabelul `greutate_panou` este pastrat ca baza pentru panouri cu table
    implicite de 0.5 mm exterior si 0.5 mm interior. Pentru alte grosimi,
    recalculam doar partea de otel si pastram aceeasi greutate de miez.
    """
    if grosime_panou_mm not in greutate_panou:
        grosimi = ", ".join(str(g) for g in sorted(greutate_panou))
        raise ValueError(f"Grosimea panoului nu exista in tabel. Grosimi disponibile: {grosimi}.")

    greutate_table_implicite = greutate_m2(
        GROSIME_TABLA_PANOU_EXTERIOR_IMPLICIT_MM + GROSIME_TABLA_PANOU_INTERIOR_IMPLICIT_MM
    )
    return max(0, greutate_panou[grosime_panou_mm] - greutate_table_implicite)


def greutate_panou_m2(
    grosime_panou_mm: int,
    grosime_tabla_exterior_mm: float | None = None,
    grosime_tabla_interior_mm: float | None = None,
    tip_panou: str | None = "perete",
) -> float:
    """Calculeaza kg/m2 pentru panou sandwich cu table exterior/interior."""
    tip_panou_norm = normalizeaza_tip_panou(tip_panou)
    exterior = (
        GROSIME_TABLA_PANOU_EXTERIOR_IMPLICIT_MM
        if grosime_tabla_exterior_mm is None
        else grosime_tabla_exterior_mm
    )
    interior = (
        GROSIME_TABLA_PANOU_INTERIOR_IMPLICIT_MM
        if grosime_tabla_interior_mm is None
        else grosime_tabla_interior_mm
    )

    if exterior <= 0 or interior <= 0:
        raise ValueError("Grosimile tablelor exterior/interior trebuie sa fie mai mari decat 0.")

    coeficient_exterior = COEFICIENT_TABLA_EXTERIOR_PANOU[tip_panou_norm]
    greutate_table = greutate_m2((exterior * coeficient_exterior) + interior)
    return greutate_miez_panou_kg_m2(grosime_panou_mm) + greutate_table


def calc_greutate_kg_m2(
    tip_produs: str,
    grosime_tabla_mm: float | None = None,
    grosime_panou_mm: int | None = None,
    grosime_tabla_exterior_mm: float | None = None,
    grosime_tabla_interior_mm: float | None = None,
    tip_panou: str | None = "perete",
) -> float:
    """Calculeaza greutatea produsului in kg/m2."""
    tip = tip_produs.strip().lower()

    if tip == "panou_sandwich":
        if grosime_panou_mm is None:
            raise ValueError("Pentru panou_sandwich trebuie furnizata grosimea panoului.")
        return greutate_panou_m2(
            grosime_panou_mm=grosime_panou_mm,
            grosime_tabla_exterior_mm=grosime_tabla_exterior_mm,
            grosime_tabla_interior_mm=grosime_tabla_interior_mm,
            tip_panou=tip_panou,
        )

    if tip in {"tabla_cutata", "profil_inalt"}:
        if grosime_tabla_mm is None:
            raise ValueError("Pentru tabla simpla trebuie furnizata grosimea tablei.")
        return greutate_m2(grosime_tabla_mm)

    raise ValueError("Tip produs invalid. Folositi: panou_sandwich, tabla_cutata sau profil_inalt.")


def calc_greutate_totala(
    tip_produs: str,
    suprafata_m2: float,
    grosime_tabla_mm: float | None = None,
    grosime_panou_mm: int | None = None,
    grosime_tabla_exterior_mm: float | None = None,
    grosime_tabla_interior_mm: float | None = None,
    tip_panou: str | None = "perete",
) -> float:
    """
    Calculeaza greutatea totala in tone.

    Pentru panouri sandwich se foloseste tabelul `greutate_panou`.
    Pentru tabla cutata/profil inalt se foloseste formula otelului simplu.
    """
    if suprafata_m2 <= 0:
        raise ValueError("Suprafata trebuie sa fie mai mare decat 0.")

    kg_m2 = calc_greutate_kg_m2(
        tip_produs=tip_produs,
        grosime_tabla_mm=grosime_tabla_mm,
        grosime_panou_mm=grosime_panou_mm,
        grosime_tabla_exterior_mm=grosime_tabla_exterior_mm,
        grosime_tabla_interior_mm=grosime_tabla_interior_mm,
        tip_panou=tip_panou,
    )

    return (kg_m2 * suprafata_m2) / 1000


def calc_emisii(greutate_tone: float, tara: str, cod_NC: str, anul: str = "2026") -> float:
    """Calculeaza emisiile implicite in tCO2."""
    if greutate_tone < 0:
        raise ValueError("Greutatea nu poate fi negativa.")

    valoare_implicita, _sursa = obtine_valoare_implicita(tara, cod_NC, anul)
    return greutate_tone * valoare_implicita


def obtine_valoare_implicita(tara: str, cod_NC: str, anul: str = "2026") -> tuple[float, str]:
    """
    Returneaza valoarea implicita tCO2/t si sursa ei.

    Sursa este `specifica_tarii` daca exista o valoare pentru tara aleasa,
    altfel `default_cod_nc` daca se foloseste valoarea generala pentru codul NC.
    """
    tara_norm = normalizeaza_tara(tara)
    cod = str(cod_NC).strip()

    sursa = "specifica_tarii"
    valori = valori_CBAM.get((tara_norm, cod))
    if valori is None:
        sursa = "default_cod_nc"
        valori = valori_CBAM.get(("default", cod))

    if valori is None:
        raise KeyError(f"Nu exista valoare implicita pentru cod_NC={cod!r}.")

    return valori.get(str(anul), valori["implicit"]), sursa


def valori_implicite_pentru_tari(anul: str = "2026") -> list[dict[str, object]]:
    """Construieste tabelul valorilor implicite afisate in frontend."""
    coduri = sorted({cod for _tara, cod in valori_CBAM})
    randuri = []

    for tara in tari_cbam:
        valori_pe_cod = {}
        surse_pe_cod = {}
        for cod in coduri:
            valoare, sursa = obtine_valoare_implicita(tara, cod, anul)
            valori_pe_cod[cod] = valoare
            surse_pe_cod[cod] = sursa
        randuri.append(
            {
                "tara": tara,
                "valori": valori_pe_cod,
                "surse": surse_pe_cod,
            }
        )

    return randuri


def calc_cost_cbam(
    emisii: float,
    pret_ETS: float,
    taxa_carbon_origine: float = 0,
) -> float:
    """
    Calculeaza costul CBAM in EUR.

    `taxa_carbon_origine` este tratata ca suma totala deja platita in tara de origine.
    Rezultatul este plafonat la 0, pentru a evita costuri negative.
    """
    if emisii < 0:
        raise ValueError("Emisiile nu pot fi negative.")
    if pret_ETS < 0:
        raise ValueError("Pretul ETS nu poate fi negativ.")
    if taxa_carbon_origine < 0:
        raise ValueError("Taxa de carbon platita nu poate fi negativa.")

    return max(0, emisii * pret_ETS - taxa_carbon_origine)


def calculeaza_cbam(
    tip_produs: str,
    suprafata_m2: float,
    tara: str,
    pret_ETS: float,
    cod_NC: str | None = None,
    grosime_tabla_mm: float | None = None,
    grosime_panou_mm: int | None = None,
    grosime_tabla_exterior_mm: float | None = None,
    grosime_tabla_interior_mm: float | None = None,
    tip_panou: str | None = "perete",
    taxa_carbon_origine: float = 0,
    anul: str = "2026",
) -> RezultatCBAM:
    """Flux complet: greutate totala, emisii implicite si cost CBAM."""
    tip = tip_produs.strip().lower()
    cod = cod_NC or COD_NC_IMPLICIT_PE_PRODUS.get(tip)
    if cod is None:
        raise ValueError("Nu se poate determina codul NC implicit pentru acest produs.")

    greutate_kg_m2 = calc_greutate_kg_m2(
        tip_produs=tip,
        grosime_tabla_mm=grosime_tabla_mm,
        grosime_panou_mm=grosime_panou_mm,
        grosime_tabla_exterior_mm=grosime_tabla_exterior_mm,
        grosime_tabla_interior_mm=grosime_tabla_interior_mm,
        tip_panou=tip_panou,
    )
    greutate_tone = (greutate_kg_m2 * suprafata_m2) / 1000
    valoare_implicita, sursa_valoare_implicita = obtine_valoare_implicita(tara, cod, anul)
    emisii_tco2 = greutate_tone * valoare_implicita
    cost_cbam_eur = calc_cost_cbam(emisii_tco2, pret_ETS, taxa_carbon_origine)
    cost_cbam_eur_m2 = cost_cbam_eur / suprafata_m2

    return RezultatCBAM(
        greutate_kg_m2=greutate_kg_m2,
        greutate_tone=greutate_tone,
        emisii_tco2=emisii_tco2,
        cost_cbam_eur=cost_cbam_eur,
        cost_cbam_eur_m2=cost_cbam_eur_m2,
        valoare_implicita=valoare_implicita,
        sursa_valoare_implicita=sursa_valoare_implicita,
    )


def citeste_float(prompt: str, implicit: float | None = None) -> float:
    valoare = input(prompt).strip()
    if valoare == "" and implicit is not None:
        return implicit
    return float(valoare.replace(",", "."))


def main() -> None:
    print("Calculator CBAM pentru panouri sandwich, tabla cutata si profil inalt")
    print("Tipuri disponibile: panou_sandwich, tabla_cutata, profil_inalt")

    tip_produs = input("Tip produs: ").strip().lower()
    suprafata_m2 = citeste_float("Suprafata importata (m2): ")
    tara = input("Tara de origine: ").strip()

    cod_implicit = COD_NC_IMPLICIT_PE_PRODUS.get(tip_produs)
    prompt_cod = f"Cod NC [{cod_implicit}]: " if cod_implicit else "Cod NC: "
    cod_NC = input(prompt_cod).strip() or cod_implicit
    if cod_NC is None:
        raise ValueError("Codul NC este obligatoriu.")

    grosime_panou_mm = None
    grosime_tabla_mm = None
    grosime_tabla_exterior_mm = None
    grosime_tabla_interior_mm = None
    tip_panou = "perete"
    if tip_produs == "panou_sandwich":
        tip_panou = input("Tip panou [perete/acoperis] [perete]: ").strip() or "perete"
        grosime_panou_mm = int(citeste_float("Grosime panou sandwich (mm): "))
        grosime_tabla_exterior_mm = citeste_float(
            f"Grosime tabla exterior (mm) [{GROSIME_TABLA_PANOU_EXTERIOR_IMPLICIT_MM}]: ",
            GROSIME_TABLA_PANOU_EXTERIOR_IMPLICIT_MM,
        )
        grosime_tabla_interior_mm = citeste_float(
            f"Grosime tabla interior (mm) [{GROSIME_TABLA_PANOU_INTERIOR_IMPLICIT_MM}]: ",
            GROSIME_TABLA_PANOU_INTERIOR_IMPLICIT_MM,
        )
    else:
        grosime_tabla_mm = citeste_float("Grosime tabla (mm): ")

    anul = input("An calcul valori implicite [2026]: ").strip() or "2026"
    pret_ETS = citeste_float("Pret EU ETS (EUR/tCO2): ")
    taxa_carbon_origine = citeste_float("Taxa carbon platita la origine, total EUR [0]: ", 0)

    rezultat = calculeaza_cbam(
        tip_produs=tip_produs,
        suprafata_m2=suprafata_m2,
        tara=tara,
        pret_ETS=pret_ETS,
        cod_NC=cod_NC,
        grosime_tabla_mm=grosime_tabla_mm,
        grosime_panou_mm=grosime_panou_mm,
        grosime_tabla_exterior_mm=grosime_tabla_exterior_mm,
        grosime_tabla_interior_mm=grosime_tabla_interior_mm,
        tip_panou=tip_panou,
        taxa_carbon_origine=taxa_carbon_origine,
        anul=anul,
    )

    print("\nRezultate:")
    print(f"Greutate pe m2: {rezultat.greutate_kg_m2:.3f} kg/m2")
    print(f"Greutate totala: {rezultat.greutate_tone:.3f} tone")
    print(f"Valoare implicita: {rezultat.valoare_implicita:.3f} tCO2/t")
    print(f"Emisii implicite: {rezultat.emisii_tco2:.3f} tCO2")
    print(f"Cost CBAM: {rezultat.cost_cbam_eur:.2f} EUR")
    print(f"Cost CBAM pe m2: {rezultat.cost_cbam_eur_m2:.2f} EUR/m2")


if __name__ == "__main__":
    main()

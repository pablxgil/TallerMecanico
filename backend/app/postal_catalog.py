from typing import TypedDict

class PostalZone(TypedDict):
    postal_code: str
    state: str
    municipality: str
    neighborhoods: list[str]

# Catálogo local limitado a Tula de Allende, Hidalgo.
TULA_POSTAL_CATALOG: list[PostalZone] = [
    {"postal_code":"42800","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Centro","Las Palmas"]},
    {"postal_code":"42803","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Bugambilias","Chapultepec","Del Llano","El Cielito","El Llano 1a Sección","El Llano 2a Sección","INFONAVIT San Marcos","Iturbe","La Huerta","Las Rosas","Lomas de Iturbe","Los Sabinos","Mastrantos","San Lorenzo","Tierra Blanca","Tultengo"]},
    {"postal_code":"42804","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Jalpa","Loma Blanca","Los Fresnos"]},
    {"postal_code":"42805","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["San José"]},
    {"postal_code":"42806","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Alvarado"]},
    {"postal_code":"42807","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Barrio Alto","El Huerto","FOVISSSTE","Las Manzanitas","Tollan"]},
    {"postal_code":"42808","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["El Salitre","PEMEX","Villas del Salitre"]},
    {"postal_code":"42809","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["La Malinche"]},
    {"postal_code":"42810","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Héroes Carranza","La Cuarta Manzana","Santa María Macua"]},
    {"postal_code":"42812","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Xiteje de la Reforma"]},
    {"postal_code":"42813","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["El Cerrito","La Milpa de García","Santa María Michimaltongo"]},
    {"postal_code":"42814","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Nantzha","San Andrés"]},
    {"postal_code":"42815","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["El Paso","La Magdalena","Xochitlán de las Flores"]},
    {"postal_code":"42816","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["La Mezquitera"]},
    {"postal_code":"42820","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["El Venado","El Vindhó","La Poza","Michimaloya","San Antonio Tula","Xiteje de Zapata"]},
    {"postal_code":"42823","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["Arboledas","Los Sauces"]},
    {"postal_code":"42824","state":"Hidalgo","municipality":"Tula de Allende","neighborhoods":["De Ferrocarrileros","San Carlos","San Pedro"]}
]

def normalize(value: str) -> str:
    return " ".join(value.casefold().split())

def by_postal_code(postal_code: str) -> PostalZone | None:
    return next((item for item in TULA_POSTAL_CATALOG if item["postal_code"] == postal_code), None)

def by_address(state: str, municipality: str, neighborhood: str) -> PostalZone | None:
    return next((item for item in TULA_POSTAL_CATALOG if normalize(item["state"]) == normalize(state) and normalize(item["municipality"]) == normalize(municipality) and any(normalize(value) == normalize(neighborhood) for value in item["neighborhoods"])), None)

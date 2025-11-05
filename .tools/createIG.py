import argparse
import json
import uuid
import xml.etree.ElementTree as ET

from colorama import just_fix_windows_console
from pathlib import Path
from termcolor import colored

just_fix_windows_console()

FHIR_NS = "http://hl7.org/fhir"
NS = {"f": FHIR_NS}
ET.register_namespace("", FHIR_NS)

IG_DIR = Path(".")

PROFILE_MAPS = {
    "core": {
        "Organization": "http://hl7.eu/fhir/base/StructureDefinition/organization-eu-core",
        "Patient": "http://hl7.eu/fhir/base/StructureDefinition/patient-eu-core",
        "Practitioner": "http://hl7.eu/fhir/base/StructureDefinition/practitioner-eu-core",
        "PractitionerRole": "http://hl7.eu/fhir/base/StructureDefinition/practitionerRole-eu-core"
    },
    "eps": {
        "AllergyIntolerance": "http://hl7.eu/fhir/eps/StructureDefinition/allergyIntolerance-eu-eps",
        "Condition": "http://hl7.eu/fhir/eps/StructureDefinition/condition-eu-eps",
        "Consent": "http://hl7.eu/fhir/eps/StructureDefinition/consent-eu-eps",
        "Device": "http://hl7.eu/fhir/eps/StructureDefinition/device-eu-eps",
        "DeviceUseStatement": "http://hl7.eu/fhir/eps/StructureDefinition/deviceUseStatement-eu-eps",
        "Flag": "http://hl7.eu/fhir/eps/StructureDefinition/flag-eu-eps",
        "Immunization": "http://hl7.eu/fhir/eps/StructureDefinition/immunization-eu-eps",
        "ImmunizationRecommendation": "http://hl7.eu/fhir/eps/StructureDefinition/immunizationRecommendation-eu-eps",
        "Medication": "http://hl7.eu/fhir/eps/StructureDefinition/Medication-eu-eps",
        "MedicationStatement": "http://hl7.eu/fhir/eps/StructureDefinition/MedicationStatement-eu-eps",
        "MedicationAdministration": "http://hl7.eu/fhir/eps/StructureDefinition/medicationAdministration-eu-eps",
        "MedicationDispense": "http://hl7.eu/fhir/eps/StructureDefinition/medicationDispense-eu-eps",
        "MedicationRequest": "http://hl7.eu/fhir/eps/StructureDefinition/medicationRequest-eu-eps",
        "Patient": "http://hl7.eu/fhir/eps/StructureDefinition/patient-eu-eps",
        "Procedure": "http://hl7.eu/fhir/eps/StructureDefinition/procedure-eu-eps",
    },
    "medication": {
        "Medication": "http://hl7.eu/fhir/mpd/StructureDefinition/Medication-eu-mpd",
        "MedicationDispense": "http://hl7.eu/fhir/mpd/StructureDefinition/MedicationDispense-eu-mpd",
        "MedicationRequest": "http://hl7.eu/fhir/mpd/StructureDefinition/MedicationRequest-eu-mpd",
        "Patient": "http://hl7.eu/fhir/base/StructureDefinition/patient-eu-core"
    },
    "lab": {
        "BodyStructure": "http://hl7.eu/fhir/laboratory/StructureDefinition/BodyStructure-eu-lab",
        "Bundle": "http://hl7.eu/fhir/laboratory/StructureDefinition/Bundle-eu-lab",
        "Composition": "http://hl7.eu/fhir/laboratory/StructureDefinition/Composition-eu-lab",
        "DiagnosticReport": "http://hl7.eu/fhir/laboratory/StructureDefinition/DiagnosticReport-eu-lab",
        "Organization": "http://hl7.org/fhir/uv/ips/StructureDefinition/Organization-uv-ips",
        "Practitioner": "http://hl7.eu/fhir/laboratory/StructureDefinition/Practitioner-eu-lab",
        "PractitionerRole": "http://hl7.eu/fhir/laboratory/StructureDefinition/PractitionerRole-eu-lab",
        "ServiceRequest": "http://hl7.eu/fhir/laboratory/StructureDefinition/ServiceRequest-eu-lab",
        "Specimen": "http://hl7.eu/fhir/laboratory/StructureDefinition/Specimen-eu-lab",
        "Substance": "http://hl7.eu/fhir/laboratory/StructureDefinition/Substance-additive-eu-lab"
    },
    "hdr": {
        "AllergyIntolerance": "http://hl7.eu/fhir/hdr/StructureDefintion/allergyIntolerance-eu-hdr",
        "Bundle": "http://hl7.eu/fhir/hdr/StructureDefinition/bundle-eu-hdr",
        "BodyStructure": "http://hl7.eu/fhir/base/StructureDefinition/BodyStructure-eu",
        "CarePlan": "http://hl7.eu/fhir/hdr/StructureDefinition/carePlan-eu-hdr",
        "Condition": "http://hl7.eu/fhir/hdr/StructureDefinition/condition-eu-hdr",
        "Consent": "http://hl7.eu/fhir/hdr/StructureDefinition/consent-eu-hdr",
        "Device": "http://hl7.eu/fhir/hdr/StructureDefinition/device-eu-hdr",
        "DeviceUseStatement": "http://hl7.eu/fhir/hdr/StructureDefinition/device-eu-hdr",
        "Encounter": "http://hl7.eu/fhir/hdr/StructureDefinition/encounter-eu-hdr",
        "FamilyMemberHistory": "http://hl7.eu/fhir/hdr/StructureDefinition/familyMemberHistory-eu-hdr",
        "Flag": "http://hl7.eu/fhir/hdr/StructureDefinition/flag-eu-hdr",
        "Immunization": "http://hl7.eu/fhir/hdr/StructureDefinition/immunization-eu-hdr",
        "ImmunizationRecommendation": "http://hl7.eu/fhir/hdr/StructureDefinition/immunizationRecommendation-eu-hdr",
        "Location": "http://hl7.eu/fhir/base/StructureDefinition/location-eu",
        "Medication": "http://hl7.eu/fhir/hdr/StructureDefinition/medication-eu-hdr",
        "MedicationAdministration": "http://hl7.eu/fhir/hdr/StructureDefinition/medicationAdministration-eu-hdr",
        "MedicationDispense": "http://hl7.eu/fhir/hdr/StructureDefinition/medicationDispense-eu-hdr",
        "MedicationRequest": "http://hl7.eu/fhir/hdr/StructureDefinition/medicationRequest-eu-hdr",
        "MedicationStatement": "http://hl7.eu/fhir/hdr/StructureDefinition/medicationStatement-eu-hdr",
        "Organization": "http://hl7.eu/fhir/base/StructureDefinition/organization-eu-core",
        "Patient": "http://hl7.eu/fhir/base/StructureDefinition/patient-eu-core",
        "Practitioner": "http://hl7.eu/fhir/base/StructureDefinition/practitioner-eu-core",
        "PractitionerRole": "http://hl7.eu/fhir/base/StructureDefinition/practitionerRole-eu-core",
        "Procedure": "http://hl7.eu/fhir/hdr/StructureDefinition/procedure-eu-hdr"
    }
}
DEPENDENCIES = {
    "core": [
        {
            "uri": "http://hl7.eu/fhir/base/ImplementationGuide/hl7.fhir.eu.base",
            "packageId": "hl7.fhir.eu.base",
            "version": "0.1.0"
        }
    ],
    "eps": [
        {
            "uri": "http://hl7.eu/fhir/eps/ImplementationGuide/hl7.fhir.eu.eps",
            "packageId": "hl7.fhir.eu.eps",
            "version": "0.0.1-ci"
        }
    ],
    "medication": [
        {
            "uri": "http://hl7.eu/fhir/mpd/ImplementationGuide/hl7.fhir.eu.mpd",
            "packageId": "hl7.fhir.eu.mpd",
            "version": "0.1.0-ballot"
        }
    ],
    "lab": [
        {
            "uri": "http://hl7.eu/fhir/laboratory/ImplementationGuide/hl7.fhir.eu.laboratory",
            "packageId": "hl7.fhir.eu.laboratory",
            "version": "0.1.1"
        }
    ],
    "hdr": [
        {
            "uri": "http://hl7.eu/fhir/hdr/ImplementationGuide/hl7.fhir.eu.hdr",
            "packageId": "hl7.fhir.eu.hdr",
            "version": "0.1.0-ballot"
        }
    ]
}

def openResource(file_path):
    resource = None
    if len(file_path.suffixes) and file_path.suffixes[-1].lower() == ".xml":
        tree = ET.parse(file_path)
        resource = tree.getroot()
    elif len(file_path.suffixes) and file_path.suffixes[-1].lower() == ".json":
        with open(file_path) as f:
            resource = json.load(f)
    else:
        print(colored(f"Not a FHIR resource: {file_path}. Skipping", "yellow"))

    return resource

def getResourceId(resource):
    try:
        if isinstance(resource, ET.Element):
            id = resource.find("f:id", NS).attrib["value"]
        elif isinstance(resource, dict):
            id = resource["id"]
    except (KeyError, AttributeError):
        return None

    return id

def addResourceId(resource, file_path):
    new_id = str(uuid.uuid4())

    if isinstance(resource, ET.Element):
        id_el = ET.Element("id")
        id_el.set("value", new_id)
        resource.insert(0, id_el)
        et = ET.ElementTree(resource)
        et.write(file_path)
    elif isinstance(resource, dict):
        resource["id"] = new_id
        with open(file_path, "w") as f:
            f.write(json.dumps(resource, indent=4))

def getResourceType(resource):
    if isinstance(resource, ET.Element):
        return resource.tag.replace("{" + FHIR_NS + "}", "")
    elif isinstance(resource, dict):
        if "resourceType" in resource:
            return resource["resourceType"]
        else:
            raise Error("JSON resource misses the 'resourceType' key")

def getCodings(resource, element_name):
    """ Get all .codings from the supplied elements as a linear list of (system, code) tuples. """
    if isinstance(resource, ET.Element):
        elements = resource.findall(f"./f:{element_name}[f:coding]", NS)
    elif isinstance(resource, dict):
        elements = resource.get(element_name)
        if not isinstance(elements, list):
            elements = [elements]

    codings = []
    for element in elements:
        if isinstance(element, ET.Element):
            for coding in element.findall(f"./f:coding[f:system][f:code]", NS):
                system = coding.find("./f:system", NS).get("value", None)
                code   = coding.find("./f:code", NS).get("value", None)
                codings.append((system, code))
        elif isinstance(element, dict):
            if "coding" in element:
                for coding in element["coding"]:
                    system = None if "system" not in coding else coding["system"]
                    code   = None if "code"   not in coding else coding["code"]
                    codings.append((system, code))
    return codings

def patientTypeForLab(resource):
    if isinstance(resource, ET.Element):
        extensions = [extension.get("url") for extension in resource.findall("./f:extension", NS)]
    elif isinstance(resource, dict):
        extensions = []
        if "extension" in resource:
            extensions = [extension["url"] for extension in resource["extension"]]
    if "http://hl7.org/fhir/StructureDefinition/patient-animal" in extensions:
        return "http://hl7.eu/fhir/laboratory/StructureDefinition/Patient-animal-eu-lab"
    else:
        return "http://hl7.eu/fhir/laboratory/StructureDefinition/Patient-eu-lab"

def observationTypeForLab(resource):
    category_codes = getCodings(resource, "category")
    if ("http://terminology.hl7.org/CodeSystem/observation-category", "laboratory") in category_codes:
        return "http://hl7.eu/fhir/laboratory/StructureDefinition/Observation-resultslab-eu-lab"
    return None

def observationTypeForEPS(resource):
    codes = getCodings(resource, "code")
    if ("http://loinc.org", "94651-7") in codes:
        return "http://hl7.eu/fhir/eps/StructureDefinition/observation-travel-eu-eps"

def observationTypeForHDR(resource):
    categories = getCodings(resource, "category")
    codes = getCodings(resource, "code")
    if ("http://terminology.hl7.org/CodeSystem/observation-category", "imaging") in categories:
        return "http://hl7.eu/fhir/hdr/StructureDefinition/observation-imgFinding-eu-hdr"
    elif ("http://terminology.hl7.org/CodeSystem/observation-category", "social-history") in categories:
        return "http://hl7.eu/fhir/hdr/StructureDefinition/observation-sdoh-eu-hdr"
    elif ("http://loinc.org", "94651-7") in codes:
        return "http://hl7.eu/fhir/hdr/StructureDefinition/observation-travel-eu-hdr"
    elif ("http://terminology.hl7.org/CodeSystem/v3-ParticipationType", "EXPAGNT") in codes:
        return "http://hl7.eu/fhir/hdr/StructureDefinition/observation-infectious-contact-eu-hdr"

def mapToProfile(resource, ig):
    resource_type = getResourceType(resource)

    profile_map = PROFILE_MAPS[ig]
    
    try:
        return profile_map[resource_type]
    except KeyError:
        if resource_type == "Patient" and ig == "lab":
            return patientTypeForLab(resource)
        if resource_type == "Observation":
            if ig == "lab":
                return observationTypeForLab(resource)
            elif ig == "eps":
                return observationTypeForEPS(resource)
            elif ig == "hdr":
                return observationTypeForHDR(resource)

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script with a required parameter.")
    parser.add_argument(
        "--ig",
        required=True,
        choices=["core", "eps", "medication", "lab", "hdr"],
        help="The ig to test against")
    args = parser.parse_args()

    resources = []

    resource_type = None
    profile = None
    resource_id = None

    for file_path in IG_DIR.glob("input/resources/*"):
        if resource := openResource(file_path):
            resource_id = getResourceId(resource)
            if not resource_id:
                print(colored(f"Resource is missing an id, so it's added for file: {file_path}", "yellow"))
                addResourceId(resource, file_path)
                resource = openResource(file_path)

            resource_type = None
            try:
                resource_type = getResourceType(resource)
            except Error as e:
                print(colored(f"Problem parsing resource: {file_path} ({e}). Skipping", "red"))
            profile = mapToProfile(resource, args.ig)
            if not profile:
                print(colored(f"No profile could be matched to resource: {file_path}. Skipping", "red"))

            if resource_type and profile and resource_id:
                resources.append({
                    "reference": {
                        "reference": f"{resource_type}/{resource_id}"
                    },
                    "exampleCanonical": profile
                })

    with open(IG_DIR / "input/IG.json") as f:
        base_ig = json.load(f)
    with open(IG_DIR / "IG_generated.json", "w") as f:
        base_ig["definition"]["resource"] = resources
        base_ig["dependsOn"] += DEPENDENCIES[args.ig]
        f.write(json.dumps(base_ig, sort_keys=False, indent=4))

    ini_path = IG_DIR / "ig.ini"
    if not ini_path.exists():
        with open(ini_path, "w") as f:
            f.write("[IG]\n")
            f.write("ig = IG_generated.json\n")
            f.write("template = #plugathon.template\n")

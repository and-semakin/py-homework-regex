import csv
import re
from collections import defaultdict
from pprint import pprint
from typing import Tuple, List, Any, Dict

from more_itertools import first_true

name_pattern = re.compile(
    r"^\s*(?P<last_name>\S+)\s*((?P<first_name>\S+)\s*)?((?P<surname>\S+)\s*)?$"
)


def get_full_name(
    last_name: str, first_name: str, surname: str
) -> Tuple[str, str, str]:
    joined_name = " ".join([last_name, first_name, surname])
    match = re.match(name_pattern, joined_name,)
    groups = match.groupdict()
    return (groups["last_name"], groups["first_name"] or "", groups["surname"] or "")


def get_phone(phone: str) -> str:
    if not phone.strip():
        return ""

    stripped_phone = "".join(re.findall(r"[+\d]|доб", phone))
    phone_match = re.match(
        (
            r"(?P<country>\+7|8)(?P<city>[\d]{3})"
            r"(?P<g1>[\d]{3})(?P<g2>[\d]{2})(?P<g3>[\d]{2})"
            r"(доб(?P<add>\d+))?"
        ),
        stripped_phone,
    )
    city = phone_match.group("city")
    g1 = phone_match.group("g1")
    g2 = phone_match.group("g2")
    g3 = phone_match.group("g3")
    add = phone_match.group("add")
    add = f" доб.{add}" if add else ""
    return f"+7({city}){g1}-{g2}-{g3}{add}"


def merge_duplicates(contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged_keys = {key: [c[key] for c in contacts] for key in contacts[0].keys()}
    return {key: first_true(values, default="") for key, values in merged_keys.items()}


if __name__ == "__main__":
    with open("phonebook_raw.csv") as f:
        reader = csv.DictReader(f, delimiter=",")
        contacts_list = list(reader)
    pprint(contacts_list)

    # fix contact names and phones
    fixed_contacts_list = []
    for contact in contacts_list:
        last_name, first_name, surname = get_full_name(
            contact["lastname"], contact["firstname"], contact["surname"]
        )
        phone = get_phone(contact["phone"])
        fixed_contacts_list.append(
            {
                **contact,
                "lastname": last_name,
                "firstname": first_name,
                "surname": surname,
                "phone": phone,
            }
        )
    pprint(fixed_contacts_list)

    # merge duplicates
    # contacts are duplicates if they have the same last name and first name
    grouped_contacts = defaultdict(list)
    for contact in fixed_contacts_list:
        grouped_contacts[(contact["lastname"], contact["firstname"])].append(contact)

    fixed_contacts_list_without_dupes = [
        merge_duplicates(group) for group in grouped_contacts.values()
    ]
    pprint(fixed_contacts_list_without_dupes)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter=",")
        # Вместо contacts_list подставьте свой список
        writer.writerows(fixed_contacts_list_without_dupes)

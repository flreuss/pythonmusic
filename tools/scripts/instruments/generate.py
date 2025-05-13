import csv


def make_instrument(patch: int, bank: int) -> int:
    assert patch >= 0 and patch <= 127
    assert bank >= 0 and patch <= 127
    return (bank << 8) | patch


# build data from source
# this also requires to substitute patch number for successive instruments

# (patch, bank, name)
data: list[tuple[int, int, str]] = []

with open("instruments.csv") as file:
    reader = csv.reader(file, delimiter=",")
    # this solution requires the first line of the csv to have a patch
    current_patch: int = 0

    for row in reader:
        _row = row.copy()
        if len(_row) == 2:
            # don't ask, this is Python; shuts up the type checker
            _row.insert(0, str(current_patch))
        else:
            current_patch = int(_row[0])

        item = (int(_row[0]), int(_row[1]), _row[2])
        data.append(item)

# HEADER
header = ""


# INSTRUMENTS
def make_doc_string(patch: int, bank: int, name: str) -> str:
    return f'''"""
Instrument constant for {name}.

This constant corresponds to the General MIDI Level 2 patch {patch}, bank {bank}.
"""'''


instruments: str = ""
keys: list[int] = []
constants: list[str] = []

for patch, bank, name in data:
    fixed_patch = patch - 1
    instrument_id = make_instrument(fixed_patch, bank)
    constant_label: str = (
        name.upper()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("+", "")
        .replace("&", "")
        .replace("'", "")
    )
    entry = f"""
{constant_label}: int = {instrument_id}
{make_doc_string(fixed_patch, bank, name)}

"""
    instruments += entry
    constants.append(constant_label)
    keys.append(instrument_id)


# __all__
all_var = "__all__ = [\n"
for constant in constants:
    all_var += f'    "{constant}",\n'
all_var += '    "INSTRUMENT_INDEX",'
all_var += "]\n\n\n"


# INDEX
instrument_index = "INSTRUMENT_INDEX: dict[int, str] = {\n"
for key, constant in zip(keys, constants):
    instrument_index += f'    {key}: "{constant}",\n'
instrument_index += '''
}
"""
An index that connects instrument ids with their name.
"""
\n\n
'''


with open("instruments.py", "w+") as file:
    file.write(header)
    file.write(all_var)
    file.write(instrument_index)
    file.write(instruments)

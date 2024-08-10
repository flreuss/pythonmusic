import csv

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


def make_doc_string(patch: int, bank: int, name: str) -> str:
    return f'''"""
Instrument constant for {name}.

This constant corresponds to the General MIDI Level 2 patch {patch}, bank {bank}.
See [General MIDI Level 2](https://en.wikipedia.org/wiki/General_MIDI_Level_2) for more information.
"""'''


instruments: str = ""

for patch, bank, name in data:
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
{constant_label}: int = _make_instrument({patch}, {bank})
{make_doc_string(patch, bank, name)}

"""
    instruments += entry


with open("instruments.py", "w+") as file:
    file.write(instruments)

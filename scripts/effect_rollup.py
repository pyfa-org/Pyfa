import os
import os.path

new_effect_file_contents = ""

for filename in os.listdir(os.path.join('eos', 'effects')):
    if filename.startswith("_") or not filename.endswith(".py") or filename == 'all.py':
        continue

    new_effect_file_contents += f"def {os.path.splitext(filename)[0]}():\n"

    file = open(os.path.join('eos', 'effects', filename), "r")

    for line in file:
        if line.strip().startswith("#") or line.strip() == "":
            continue
        new_effect_file_contents += f"    {line}"

    new_effect_file_contents += "\n    return locals()\n\n"

with open(os.path.join('eos', 'effects', 'all.py'), "w") as f:
    f.write(new_effect_file_contents)



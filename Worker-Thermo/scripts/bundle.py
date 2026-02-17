from json import dumps
from pathlib import Path
from zipfile import ZipFile

SRC     = Path('.')
DEST    = Path('./package.json')
VERSION = '0.0.0'

files = []

exclusions = [
    'scripts',
    'tests',
    'venv',
]

with ZipFile('bundle.zip', 'w') as zip_file:
    for path in SRC.rglob('*.py'):
        if any(exclusion in path.parts for exclusion in exclusions):
            continue

        if path.is_file():
            relative_path = path.relative_to(SRC).as_posix()

            zip_file.write(path, relative_path)

            files.append([
                relative_path,
                relative_path,
            ])

    package_json = {
        'version' : VERSION,
        'urls'    : files,
    }

    DEST.parent.mkdir(exist_ok=True)
    DEST.write_text(dumps(package_json, indent=4))

    zip_file.write(DEST, DEST.name)

    DEST.unlink()

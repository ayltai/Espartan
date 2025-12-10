from pathlib import Path
from setuptools import find_packages, setup

def read_requirements(filename: str):
    return [line.strip() for line in Path(filename).read_text().splitlines() if line.strip() and not line.startswith("#")]

production_requirements = read_requirements('requirements.txt')
extra_requirements      = read_requirements('requirements.dev.txt')

setup(
    name='espartan-master',
    version='0.1.0',
    packages=find_packages(),
    install_requires=production_requirements,
    extras_require={
        'dev': extra_requirements,
    },
)

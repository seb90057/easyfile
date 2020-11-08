import setuptools
import data_dictionary

with open("requirements/common.txt") as handler:
    install_requires = handler.readlines()

setuptools.setup(
    install_requires=install_requires,
    name=data_dictionary,
    package_data={
        "data_dictionary.config": ["config.ini"],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    scripts=["scripts/run.sh"],
    version=data_dictionary.__version__,
)

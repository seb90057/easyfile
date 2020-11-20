import setuptools

with open("requirements/common.txt") as handler:
    install_requires = handler.readlines()

setuptools.setup(
    install_requires=install_requires,
    name="sde_easy_file",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    version="1.0.5",
    author="SDE",
    url="https://github.com/seb90057/easyfile",
    author_email="seb.delarue@gmail.com",
)

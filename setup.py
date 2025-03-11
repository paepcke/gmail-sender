from setuptools import setup, find_packages

setup(
    name="gmail-sender",
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)

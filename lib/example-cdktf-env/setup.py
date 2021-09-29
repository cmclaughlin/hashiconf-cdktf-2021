from setuptools import find_packages, setup

requires = [
    "deepmerge==0.1.1",
    "envyaml==0.2060",
    "boto3>=1.15.3",
]

name = "example-cdktf-env"

setup(
    name=name,
    version="1.0.0",
    url="https://github.example.com/example/cdktf.git",
    author="Example",
    author_email="example@example.com",
    description=name,
    packages=find_packages(),
    install_requires=requires,
    setup_requires=requires,
    include_package_data=True,
)

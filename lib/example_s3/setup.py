from setuptools import find_packages, setup

requires = [""]

name = "example_s3"

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

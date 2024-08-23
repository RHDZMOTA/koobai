import os
from setuptools import setup, find_packages

# Environ variables
CODEBASE_PATH = os.environ.get(
    "CODEBASE_PATH",
    default=os.path.join("src", "main")
)

with open("README.md", "r") as file:
    readme = file.read()

with open("requirements.txt", "r") as file:
    requirements = [
        req.strip()
        for req in file.read().splitlines()
        if req and not req.startswith("#")
    ]


version_filename = "version"
version_filepath = os.path.join(
    CODEBASE_PATH,
    "koobai",
    version_filename,
)

with open(version_filepath, "r") as file:
    version = file.readline().strip()


setup(
    name="koobai",
    version=version,
    description=(
        "KOOBAI"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Rodrigo H. Mota",
    author_email="info@rhdzmota.com",
    url="https://github.com/rhdzmota/koobai",
    classifiers=[
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={
        "": CODEBASE_PATH,
    },
    package_data={
        "": [
            os.path.join(
                "koobai",
                "version",
            ),
        ],
    },
    packages=[
        package
        for package in find_packages(where=CODEBASE_PATH)
        if package.startswith("koobai")
    ],
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10, <4",
    license="TBD",
    zip_safe=False,
)

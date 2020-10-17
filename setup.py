"""Package Setup File"""
import setuptools

with open("README.md") as readme_file:
    README = readme_file.read()

with open("HISTORY.md") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ["numpy", "pandas"]
TEST_REQUIREMENTS = ["pytest"]
EXTRAS_REQUIRE = {
    "dev": [
        "pylint",
        "black",
        "pre-commit",
    ] + TEST_REQUIREMENTS,
}

setuptools.setup(
    author="Lukas Koning",
    author_email="lukas.koning@afm.nl",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Data Quality checks.",
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    long_description=README + "\n\n" + HISTORY,
    keywords="data validation, data quality, data checks, data expectations",
    name="validata",
    version="0.1.0",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/LFKoning/validata",
)

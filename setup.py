from setuptools import find_packages, setup

setup(
    name="repo-filter",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "dill",
        "git-filter-repo",
        "GitPython",
        "questionary",
        "rich",
    ],
    entry_points={"console_scripts": ["repo-filter = main:cli"]},
)

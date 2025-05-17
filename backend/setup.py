from setuptools import setup, find_packages

setup(
    name="artist-ranking",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "sqlalchemy",
    ],
) 
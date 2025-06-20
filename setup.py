# setup.py
from setuptools import setup, find_packages
from dotenv import load_dotenv
import os

def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(req_path) as f:
        return f.read().splitlines()

# Load environment variables
load_dotenv()
AUTHOR_EMAIL = os.getenv('AUTHOR_EMAIL', "default@example.com")

setup(
    name='YouTubeWikiBot',
    version='0.1.1',
    author='Luis Imperial',
    author_email=AUTHOR_EMAIL,
    description='A bot to create a database of the most popular creators on YouTube.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LuisAPI/YouTubeWikiBot',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
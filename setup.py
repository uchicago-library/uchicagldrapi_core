from setuptools import setup
from setuptools import find_packages

def readme():
    with open("README.md", 'r') as f:
        return f.read()

setup(
    name = "uchicagoldrapicore",
    description = "The UChicago LDR API core package.",
    long_description = readme(),
    version = "0.0.1dev",
    author = "Brian Balsamo, Tyler Danstrom",
    author_email = "balsamo@uchicago.edu, tdanstrom@uchicago.edu",
    packages = find_packages(
        exclude = [
            "build",
            "bin",
            "dist",
            "tests",
            "uchicagoldrapicore.egg-info"
        ]
    ),
    install_requires = [
        "flask",
        "flask_restful",
        "flask_login",
        "itsdangerous"
    ],
    entry_points = {
        'console_scripts':[
            'ldrapidebugserver = uchicagoldrapicore.bin.rundebugserver:main',
            'makesecretkey = uchicagoldrapicore.bin.makesecretkey:main'
        ]
    },
    include_package_data=True,
    data_files = [
        ('config', ['config.ini'])
    ]
)

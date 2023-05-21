from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='kube-connector',
    version='0.1Beta',
    author='Ali Jawad FAHS',
    author_email='alijawadfahs@gmail.com',
    description='kube-connector',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'kube-connector=src.main:main',
        ],
    },
)
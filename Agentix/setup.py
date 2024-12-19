from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='agentix',
    version='0.1.5',
    packages=find_packages(),
    description='A framework for building agentic systems with minimal boilerplate.',
    long_description=readme(),
    entry_points={
        'console_scripts': [
            'agentix=agentix.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
 
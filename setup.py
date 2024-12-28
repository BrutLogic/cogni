from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='cogni',
    version='0.1.0',
    packages=find_packages(),
    description='A framework for building agentic systems with minimal boilerplate.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/cogni',
    install_requires=[
        'fire>=0.5.0',
        'rich>=13.0.0',
        'pytest>=7.0.0',
    ],
    entry_points={
        'console_scripts': [
            'cogni=cogni.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)

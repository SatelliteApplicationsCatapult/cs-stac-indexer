from setuptools import setup, find_packages

setup(
    author='Juan Emilio Zurita Macias',
    author_email='juanezm@ieee.org',
    name='cs-indexing-tools',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=['click~=7.1.2', 'elasticsearch==7.10.1'],
    entry_points={
        'console_scripts': ['stac-to-es=stac_to_es.cli:main'],
    }
)

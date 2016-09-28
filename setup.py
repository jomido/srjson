from setuptools import setup, find_packages

setup(
    name='srjson',
    version='0.1',
    description='self-referential json',
    url='https://github.com/jomido/srjson',
    author='Jonathan Dobson',
    author_email='jon.m.dobson@gmail.com',
    license='MIT',
    packages=find_packages(),
    provides=['srjson'],
    test_suite='pytest',
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    install_requires=[],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "srjson = srjson:main"
        ]
    }
)

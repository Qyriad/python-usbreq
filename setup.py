from setuptools import setup, find_packages

setup(
    name='usbreq',
    version='0.2.1',
    license='MIT',
    url='https://github.com/Qyriad/python-usbreq',
    author='Mikaela Szekely',
    author_email='mikaela.szekely@qyriad.me',
    description='A USB library for humans',
    readme = 'README.md',
    platforms='any',
    python_requires='>= 3.9',
    packages=find_packages(),
    install_requires=['pyusb', 'inflection'],
    setup_requires=['setuptools'],
    extras_require={
        'docs': 'sphinx-rtd-theme',
    },

    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: System :: Hardware :: Universal Serial Bus (USB)',
    ],
)

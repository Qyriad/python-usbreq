from setuptools import setup, find_packages

setup(
    name='usbreq',
    version='0.1',
    license='MIT',
    url='https://github.com/Qyriad/python-usbreq',
    author='Mikaela Szekely',
    author_email='mikaela.szekely@qyriad.me',
    description='A PyUSB wrapper library for quick testing and prototyping',
    platforms='any',
    packages=find_packages(),
    install_requires=['pyusb', 'inflection'],
    setup_requires=['setuptools'],

    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
    ],
)

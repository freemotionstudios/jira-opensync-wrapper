from setuptools import setup, find_packages

setup(
    name='jira-opensync-wrapper',
    version='0.1.0',
    description='Python class to add specific functionality to the JIRA python package',
    author='Dan',
    author_email='dan@example.com',
    url='https://github.com/freemotionstudios/jira-opensync-wrapper',
    packages=find_packages(),
    install_requires=[
        'jira',
        'pytest',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

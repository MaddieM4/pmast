from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pmast',
    version='0.1.1',

    description='Pattern Matching for the Python AST',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    url='https://github.com/campadrenalin/pmast',
    author='Philip Horger',
    author_email='campadrenalin@gmail.com',
    packages=['pmast'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    zip_safe=True,
)

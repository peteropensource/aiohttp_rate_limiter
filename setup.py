from setuptools import setup

setup(
    name='aiohttp_client_rate_limiter',
    version='1.0.2',
    description='This is a mini tool that overwrite aiohttp session to provide rate limit function within a same session.',
    long_description='This is a mini tool that overwrite aiohttp session to provide rate limit function within a same session.',
    author='Peter Lee',
    author_email='info@peterlee.space',
    url='https://github.com/peteropensource/aiohttp_rate_limiter',
    packages=['aiohttp_client_rate_limiter'],
    install_requires=[
        # List any dependencies required by your package
        "aiohttp>=3.8.5",
        "aiosignal>=1.3.1",
        "async-timeout==4.0.2",
        "attrs==23.1.0",
        "charset-normalizer==3.2.0",
        "frozenlist==1.4.0",
        "idna==3.4",
        "multidict==6.0.4",
        "yarl==1.9.2",
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        # Add any relevant classifiers for your package
    ],
)
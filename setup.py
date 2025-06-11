import setuptools

with open("README.rst", "r") as f:
    README = f.read()


setuptools.setup(
    name="newrelic-lambda",
    description="New Relic Lambda",
    long_description=README,
    long_description_content_type="text/x-rst",
    license="New Relic License",
    version="0.1.6",
    author="New Relic",
    author_email="support@newrelic.com",
    install_requires=("newrelic>=5.12.0.140",),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    zip_safe=False,
)

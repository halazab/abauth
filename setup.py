from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="halazb-abauth",
    version="0.1.3",
    author="Halazab",
    author_email="halazb27@gmail.com",
    description="A comprehensive Django authentication system with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/halazab/abauth",
    project_urls={
        "Bug Tracker": "https://github.com/halazab/abauth/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "Django",
        "djangorestframework",
        "djangorestframework-simplejwt",
        "django-cors-headers",
        "qrcode",
        "Pillow",
        "python-dotenv",
        "django-redis",
        "django-ratelimit",
        "django-filter",
        "django-cleanup",
        "django-storages",
        "django-allauth",
    ],
    include_package_data=True,
    zip_safe=False,
) 
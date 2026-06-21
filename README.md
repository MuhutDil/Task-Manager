### Hexlet tests and linter status:
[![Actions Status](https://github.com/MuhutDil/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MuhutDil/python-project-52/actions)
[![PyCI](https://github.com/MuhutDil/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/MuhutDil/python-project-52/actions/workflows/pyci.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=MuhutDil_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=MuhutDil_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MuhutDil_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MuhutDil_python-project-52)

# Task Manager
Task Manager is a website for managing various tasks. \
To access the full functionality of the site, registration is required.
This will grant you access to the following features:
- Editing and deleting your profile.
- Adding, viewing, updating and deleting statuses (if not assigned to any task)
- Adding, viewing, updating and deleting labels (if not assigned to any task)
- Adding, viewing, search, updating and deleting task (for owner only)

## Demo version of the site
[Render](https://python-project-52-sxu3.onrender.com)

The service is available in 2 languages (English and Russian)

## Installation
### Prerequisites
- Python version 3.10 or higher
- Django version 5.2 or higher
- PostgreSQL version 16.6 or higher
- Uv version 0.5 or higher (optional)

### Download
    git clone https://github.com/MuhutDil/Task-Manager

### Configuration
Rename the `.env_example` file to `.env` and following the example in this file, enter your data.

`Makefile` simplifies the installation and startup process.
#### Build the application and preparation for launch
    make build
#### Starting a local development server
    make dev
#### Starting a production (working) server
    make start

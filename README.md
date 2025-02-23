# Django testing

## Descriptions

This project is to show how to test content, logic and routes of the Django application using Pytest and Unittest.

## Requirements

- **OS**: Linux
- **Python 3.8**: to work with the project, you need to have Python version 3.8 or later installed. Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **pip**: Python package manager. Download pip: [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

## Project launch
The project includes two Django applications. To start them, it's needed to create working environment and install requirements:

```bash
git clone git@github.com:aleksej-tulko/drf_django_testing.git
cd drf_django_testing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Unittest
To test the project with Unittest, navigate to ya_note/ and start application:

```bash
cd ya_note/
python3 manage.py migrate
python3 manage.py runserver
```

Open new terminal and start tests:

```bash
python3 manage.py test
```

### Pytest
To check Pytest, move to ya_news/ and start it:

```bash
cd ya_news/
python3 manage.py migrate
python3 manage.py runserver
```

Just run this in the new terminal:

```bash
pytest
```

## Author
[Aliaksei Tulko](https://github.com/aleksej-tulko)
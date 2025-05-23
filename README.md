<!-- filepath: c:\Users\gramo\Desktop\sites\artyap-server\artyap\README.md -->

# ArtYap Server

**Client Repository:** [https://github.com/GramosTV/artyap-client](https://github.com/GramosTV/artyap-client)

ArtYap Server is a Django-based application that serves data from the Art Institute of Chicago. It uses a local copy of the data, which needs to be set up as described below.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Pip (Python package installer)
- Git (for cloning the repository, optional)
- MySQL (or another database compatible with Django, configured in `my_project/settings.py`)

## Installation

1. **Clone the repository (optional):**

   ```bash
   git clone <your-repository-url>
   cd artyap-server/artyap
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Data Setup

This server utilizes data from the [Art Institute of Chicago API data repository](https://github.com/art-institute-of-chicago/api-data).

1. Download or clone the `artic-data` repository.
2. Place the `artic-data` folder in the root directory of this project (i.e., alongside `manage.py` and `README.md`).

## Running the Server

1. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

2. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The server will typically be available at `http://127.0.0.1:8000/`.

## API Endpoints

(Details about the available API endpoints will be added here. For now, you can explore the `my_app/urls.py` and `my_app/views.py` to understand the available routes.)

- `/api/...`
- ...

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST framework](https://www.django-rest-framework.org/) - For building Web APIs
- [Python Decouple](https://pypi.org/project/python-decouple/) - For separating settings from code
- [MySQL Connector/Python](https://pypi.org/project/mysqlclient/) - MySQL driver

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information (if a license file is added).

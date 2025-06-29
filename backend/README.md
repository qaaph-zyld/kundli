# Vedic Kundli Calculator Backend

This is the backend service for the Vedic Kundli Calculator application, providing astrological calculations and API endpoints for the frontend application.

## Architecture

The backend follows a clean architecture approach with the following components:

- **Core**: Contains domain entities, use cases, and repository interfaces
- **Infrastructure**: Contains implementations of repositories, services, and adapters
- **API**: Contains API routes, controllers, and middleware

## Features

- Multi-provider astronomical calculation protocol
- Birth chart calculation with planetary positions, house cusps, and aspects
- Divisional charts (vargas) calculation
- Dasha periods calculation
- Yoga identification
- Performance profiling and metrics
- User profile management

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
cd src
python main.py
```

The API will be available at http://localhost:8000

### API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

The application can be configured using environment variables or a `.env` file in the backend directory. Available configuration options:

- `HOST`: Host to bind the server to (default: 0.0.0.0)
- `PORT`: Port to bind the server to (default: 8000)
- `RELOAD`: Whether to enable auto-reload for development (default: False)

## Calculator Providers

The application supports multiple calculator providers:

- **VedicastroCalculator**: Uses the vedicastro library
- **SwissEphemerisCalculator**: Uses the pyswisseph library

The calculator provider can be configured using the `/birth-charts/config` endpoint.

## Development

### Project Structure

```
backend/
├── requirements.txt
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── routes/
│   │   └── app.py
│   ├── core/
│   │   ├── entities/
│   │   ├── repositories/
│   │   └── use_cases/
│   ├── infrastructure/
│   │   ├── astro/
│   │   ├── database/
│   │   └── repositories/
│   └── main.py
└── tests/
    ├── api/
    ├── core/
    └── infrastructure/
```

### Testing

Run tests using pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License.

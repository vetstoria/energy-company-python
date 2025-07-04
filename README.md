## Requirements

The project requires [Python 3.12](https://www.python.org/downloads/release/python-3120/) or higher and the [Poetry](https://python-poetry.org/) package manager.

## Useful Python commands

### Installation

After installing poetry, install the project dependencies with:

```console
poetry install --with ci,tests
```
This will install main dependencies together with optional ones.
For more information see [optional groups](https://python-poetry.org/docs/managing-dependencies#optional-groups) settings.

### Run the tests

Run all tests

```console
poetry run pytest
```

### Run the application

Run the application which will be listening on port `8020`.

```console
poetry run python app.py
```

### Building Docker Image
The application can be containerized by using:
```console
docker build -t energy-company .
```

### Building Docker image
Once the docker image is built, it can be run with:
```console
docker run -p 8020:8020 energy-company
```

## API

Below is a list of API endpoints with their respective input and output. Please note that the application needs to be
running for the following endpoints to work. For more information about how to run the application, please refer
to [run the application](#run-the-application) section above.

### Autogenerated documentations
The application will automatically generate documentations and provide them under:

- [Swagger UI](https://github.com/swagger-api/swagger-ui) > http://localhost:8020/docs
- [ReDoc](https://github.com/Redocly/redoc) > http://localhost:8020/redoc

### Store Readings

Endpoint

```text
POST /readings/store
```

Example of body

```json
{
  "smartMeterId": <smartMeterId>,
  "electricityReadings": [
    {
      "time": <timestamp>,
      "reading": <reading>
    }
  ]
}
```

Parameters

| Parameter      | Description                                           |
| -------------- | ----------------------------------------------------- |
| `smartMeterId` | One of the smart meters' id listed above              |
| `time`         | The date/time (as epoch) when the _reading_ was taken |
| `reading`      | The consumption in `kW` at the _time_ of the reading  |

Example readings

| Date (`GMT`)      | Epoch timestamp | Reading (`kW`) |
| ----------------- | --------------: | -------------: |
| `2020-11-29 8:00` |      1606636800 |         0.0503 |
| `2020-11-29 8:01` |      1606636860 |         0.0621 |
| `2020-11-29 8:02` |      1606636920 |         0.0222 |
| `2020-11-29 8:03` |      1606636980 |         0.0423 |
| `2020-11-29 8:04` |      1606637040 |         0.0191 |

The following POST request, is an example request using CURL, sends the readings shown in the table above.

```console
curl \
  -X POST \
  -v \
  -H "Content-Type: application/json" \
  "http://localhost:8020/readings/store" \
  -d '{"smartMeterId":"smart-meter-0","electricityReadings":[{"time":1606636800,"reading":0.0503},{"time":1606636860,"reading":0.0621},{"time":1606636920,"reading":0.0222},{"time":1606636980,"reading":0.0423},{"time":1606637040,"reading":0.0191}]}'
```

The above command will return the submitted readings.

```json
{
  "electricityReadings": [
    {
      "reading": 0.0503,
      "time": 1606636800
    },
    {
      "reading": 0.0621,
      "time": 1606636860
    },
    {
      "reading": 0.0222,
      "time": 1606636920
    },
    {
      "reading": 0.0423,
      "time": 1606636980
    },
    {
      "reading": 0.0191,
      "time": 1606637040
    }
  ],
  "smartMeterId": "smart-meter-0"
}
```

### Get Stored Readings

Endpoint

```text
GET /readings/read/<smartMeterId>
```

Parameters

| Parameter      | Description                              |
| -------------- | ---------------------------------------- |
| `smartMeterId` | One of the smart meters' id listed above |

Retrieving readings using CURL

```console
curl "http://localhost:8020/readings/read/smart-meter-0"
```

Example output

```json
[
  {
    "reading": 0.0503,
    "time": 1606636800
  },
  {
    "reading": 0.0621,
    "time": 1606636860
  },
  {
    "reading": 0.0222,
    "time": 1606636920
  },
  {
    "reading": 0.0423,
    "time": 1606636980
  },
  {
    "reading": 0.0191,
    "time": 1606637040
  },
  {
    "reading": 0.988,
    "time": 989707945
  },
  {
    "reading": 0.402,
    "time": 992419009
  },
  {
    "reading": 0.785,
    "time": 1006196973
  },
  {
    "reading": 0.327,
    "time": 989837737
  },
  {
    "reading": 0.485,
    "time": 1003722501
  }
]
```

### View Current Price Plan and Compare Usage Cost Against all Price Plans

Endpoint

```text
GET /price-plans/compare-all/<smartMeterId>
```

Parameters

| Parameter      | Description                              |
| -------------- | ---------------------------------------- |
| `smartMeterId` | One of the smart meters' id listed above |

Retrieving readings using CURL

```console
curl "http://localhost:8020/price-plans/compare-all/smart-meter-0"
```

Example output

```json
{
  "pricePlanComparisons": [
    {
      "price-plan-2": 1.8573933524727018e-06
    },
    {
      "price-plan-1": 3.7147867049454036e-06
    },
    {
      "price-plan-0": 1.8573933524727016e-05
    }
  ],
  "pricePlanId": "price-plan-0"
}
```

### View Recommended Price Plans for Usage

Endpoint

```text
GET /price-plans/recommend/<smartMeterId>[?limit=<limit>]
```

Parameters

| Parameter      | Description                                          |
| -------------- | ---------------------------------------------------- |
| `smartMeterId` | One of the smart meters' id listed above             |
| `limit`        | (Optional) limit the number of plans to be displayed |

Retrieving readings using CURL

```console
curl "http://localhost:8020/price-plans/recommend/smart-meter-0?limit=2"
```

Example output

```json
[
  {
    "price-plan-2": 1.8573933524727018e-06
  },
  {
    "price-plan-1": 3.7147867049454036e-06
  }
]
```

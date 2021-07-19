# SaltyCoin

[![Python 3.9](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/downloads/release/python-390/)

SaltyCoin is a server that simulates the price of a imaginary currency over time.

## Major Libraries Used
- [APScheduler](https://apscheduler.readthedocs.io/en/stable/#)
- [NumPy](https://numpy.org/)
- [Quart](https://pgjones.gitlab.io/quart/)
- [RX](http://reactivex.io/)

## Installation

```bash
pip install -r requirements.txt
```

## Deployment
```bash
python app.py
```
The app will attempt to read variables from the `.env` if it is present.


## API Documentation

### GET: api/cat
Always returns a cat.
```json
// Example response
~(=^..^)
```

### GET: api/values
Gets a list of the last 100 values with the oldest value as the first element in the list.
```json
// Example response
{
    "values": [
        9.957677715722722,
        9.973286108982947,
        10.169675737607,
        ...
    ]
}
```

### GET: api/values/future
Keeps the connection open until the next time a value is generated. Then returns a list of the last 100 values with the oldest value as the first element in the list.
```json
// Example response
{
    "values": [
        9.957677715722722,
        9.973286108982947,
        10.169675737607,
        ...
    ]
}
```

### GET: api/config
Gets the current parameters of the random walker.
```json
// Example response
{
  "minimum": 0.01,
  "skew": 0,
  "volatility": 0.01
}
```

### GET: api/config/future
Keeps the connection open until the next time the random walker's config changes. Then returns the current config parameters of the random walker.
```json
// Example response
{
  "minimum": 0.01,
  "skew": 0,
  "volatility": 0.01
}
```

### POST: api/config
Updates the config parameters of the random walker. Properties that aren't specified in the request payload will be ignored and unchanged. An `x-api-key` header is required to authenticate.
```json
// Example request
{
  "minimum": 0.01,
  "skew": 0,
  "volatility": 0.01
}
```

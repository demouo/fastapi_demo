# fastapi_demo

A simple FastAPI demo with background crawl task.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API

- `POST /crawl` - Start crawl task (body: `{"url": "https://example.com"}`)
- `GET /result/{task_id}` - Get crawl result by task_id

## Test

```bash
# Start crawl
curl -X POST http://localhost:8000/crawl -H "Content-Type: application/json" -d '{"url":"https://www.baidu.com"}'

# Get result
curl http://localhost:8000/result/{task_id}
```

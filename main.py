from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict
import httpx
import uuid

# 存储任务结果
tasks: Dict[str, str] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # 清理资源
    tasks.clear()

app = FastAPI(lifespan=lifespan)


class CrawlRequest(BaseModel):
    url: str


class TaskResponse(BaseModel):
    task_id: str
    message: str


class ResultResponse(BaseModel):
    task_id: str
    status: str
    result: str = None


async def fetch_url(task_id: str, url: str):
    """后台任务：爬取URL源码"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            tasks[task_id] = response.text
    except Exception as e:
        tasks[task_id] = f"Error: {str(e)}"


@app.post("/crawl", response_model=TaskResponse)
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    """
    启动爬取任务
    - 输入URL，后台爬取页面源码
    """
    task_id = str(uuid.uuid4())
    background_tasks.add_task(fetch_url, task_id, request.url)
    return TaskResponse(task_id=task_id, message="Crawl task started")


@app.get("/result/{task_id}", response_model=ResultResponse)
async def get_result(task_id: str):
    """
    获取爬取结果
    - 根据task_id查询结果
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return ResultResponse(task_id=task_id, status="completed", result=tasks[task_id])

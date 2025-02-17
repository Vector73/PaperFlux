import asyncio
import aiohttp
from pymongo import MongoClient
from datetime import datetime, timezone
import os

API_URL = "https://huggingface.co/api/daily_papers"
PDF_BASE_URL = "https://arxiv.org/pdf/{id}.pdf"

client = MongoClient("mongodb://localhost:27017/")
db = client["papers_summary_database"]
collection = db["papers"]


async def fetch_papers(session):
    async with session.get(API_URL) as response:
        if response.status == 200:
            return await response.json()
        raise Exception(f"API request failed: {response.status}")


async def download_pdf(session, paper_entry):
    try:
        paper_id = paper_entry["paper"]["id"]
        pdf_url = PDF_BASE_URL.format(id=paper_id)

        async with session.get(pdf_url) as response:
            if response.status == 200:
                content = await response.read()
                os.makedirs("pdfs", exist_ok=True)
                with open(f"pdfs/{paper_id}", "wb") as f:
                    f.write(content)

                return (paper_id, True)

            return (paper_id, False)
    except Exception as e:
        print(f"Error downloading {paper_id}: {str(e)}")
        return (paper_id, False)


async def run_paper_fetch_job():
    async with aiohttp.ClientSession() as session:
        papers = await fetch_papers(session)
        tasks = []

        for paper in papers:
            paper_data = paper["paper"]
            paper_data["fetchedAt"] = datetime.now(timezone.utc).isoformat()
            collection.insert_one(paper_data)

        tasks = [download_pdf(session, paper) for paper in papers]
        results = await asyncio.gather(*tasks)

        successful = sum(1 for _, status in results if status)
        print(f"Downloaded {successful}/{len(papers)} papers successfully")

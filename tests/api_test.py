import aiohttp
import asyncio
import os
from datetime import datetime

API_URL = "https://huggingface.co/api/daily_papers"
PDF_BASE_URL = "https://arxiv.org/pdf/{id}.pdf"
DOWNLOAD_DIR = "papers"

async def fetch_papers(session):
  async with session.get(API_URL) as response:
    if response.status == 200:
        return await response.json()
    raise Exception(f"API request failed: {response.status}")

async def download_pdf(session, paper_entry):
  try:
    paper_id = paper_entry["paper"]["id"]
    pdf_url = PDF_BASE_URL.format(id=paper_id)
    clean_id = paper_id.replace("/", "_")
    filename = f"{datetime.now().date()}_{clean_id}.pdf"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    async with session.get(pdf_url) as response:
        if response.status == 200:
            content = await response.read()
            with open(filepath, "wb") as f:
                f.write(content)
            return (paper_id, True)
        return (paper_id, False)
  except Exception as e:
    print(f"Error downloading {paper_id}: {str(e)}")
    return (paper_id, False)
  
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def main():
    async with aiohttp.ClientSession() as session:
        papers = await fetch_papers(session)
        print(f"Found {len(papers)} papers")
        
        print(f"\nFound {len(papers)} papers:")
        for i, paper_entry in enumerate(papers, 1):
            paper = paper_entry.get("paper", {})
            print(f"\nPaper {i}:")
            print(f"ID: {paper.get('id')}")
            print(f"Title: {paper.get('title')}")
            print(f"Authors: {', '.join([author.get('name') for author in paper.get('authors', [])])}")
            print(f"Published: {paper.get('publishedAt')}")
            print(f"Summary: {paper.get('summary')[:200]}...")
            print(f"PDF URL: {PDF_BASE_URL.format(id=paper.get('id'))}")

        tasks = [download_pdf(session, paper) for paper in papers]
        results = await asyncio.gather(*tasks)
        
        successful = sum(1 for _, status in results if status)
        print(f"Downloaded {successful}/{len(papers)} papers successfully")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from src.services.paper_fetcher import PaperFetcher
from src.services.paper_analyzer import PaperAnalyzer
from src.services.database import DatabaseService

class PaperProcessingScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.fetcher = PaperFetcher()
        self.analyzer = PaperAnalyzer()
        self.db = DatabaseService()
        self._running = False

    async def process_papers(self):
        if self._running:
            print("Previous processing still running, skipping...")
            return

        self._running = True
        print("Starting daily paper processing...")
        
        try:
            self.db.clear_collection()
            papers = await self.fetcher.fetch_papers()
            
            for paper in papers:
                if not self._running:  # Check if we should stop
                    break
                    
                pdf_path = await self.fetcher.download_paper(paper)
                if pdf_path:
                    try:
                        explanation = self.analyzer.analyze_paper(pdf_path)
                        paper_obj = self.fetcher.parse_paper_data(paper)
                        paper_obj.explanation = explanation
                        self.db.insert_paper(paper_obj)
                    finally:
                        if os.path.exists(pdf_path):
                            os.remove(pdf_path)
                            
        except Exception as e:
            print(f"Error in paper processing: {str(e)}")
        finally:
            self._running = False

    def start(self):
        self.scheduler.add_job(
            lambda: asyncio.run(self.process_papers()),
            'cron',
            hour=0,
            minute=0,
            next_run_time=datetime.now()
        )
        self.scheduler.start()

    def stop(self):
        self._running = False
        self.scheduler.shutdown()
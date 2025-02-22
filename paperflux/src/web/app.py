import gradio as gr
from src.services.database import DatabaseService

class PaperFluxUI:
    def __init__(self):
        self.db = DatabaseService()
        self.papers = self.db.get_all_papers()
        self.current_index = 0

    def get_current_paper(self):
        if not self.papers:
            return {
                "title": "No papers available", 
                "explanation": "Please wait for papers to be processed.", 
                "pdf_url": ""
            }
        paper = self.papers[self.current_index]
        authors = ", ".join([author["name"] for author in paper["authors"]])
        title = f"# {paper['title']}\n\nAuthors: {authors}"
        return {
            "title": title,
            "explanation": paper["explanation"],
            "pdf_url": paper["pdf_url"]
        }

    def next_paper(self):
        if self.current_index < len(self.papers) - 1:
            self.current_index += 1
        return self.get_current_paper()

    def previous_paper(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_current_paper()

    def create_interface(self):
        with gr.Blocks(theme=gr.themes.Base()) as interface:
            title = gr.Markdown()
            explanation = gr.Markdown()
            
            # Create an HTML component for the download link
            download_html = gr.HTML()
            
            with gr.Row():
                prev_btn = gr.Button("Previous Paper")
                next_btn = gr.Button("Next Paper")

            def update_ui(paper_data):
                download_link = f"""
                <div style="text-align: center; margin-top: 10px;">
                    <a href="{paper_data['pdf_url']}" target="_blank" 
                       style="text-decoration: none;">
                        <button style="padding: 10px 20px; background-color: #4CAF50; 
                                     color: white; border: none; border-radius: 5px; 
                                     cursor: pointer;">
                            Download Paper
                        </button>
                    </a>
                </div>
                """
                return (
                    paper_data["title"],
                    paper_data["explanation"],
                    download_link
                )

            next_btn.click(
                fn=lambda: update_ui(self.next_paper()),
                outputs=[title, explanation, download_html]
            )
            
            prev_btn.click(
                fn=lambda: update_ui(self.previous_paper()),
                outputs=[title, explanation, download_html]
            )

            # Initialize with first paper
            paper_data = self.get_current_paper()
            init_download_link = f"""
            <div style="text-align: center; margin-top: 10px;">
                <a href="{paper_data['pdf_url']}" target="_blank" 
                   style="text-decoration: none;">
                    <button style="padding: 10px 20px; background-color: #4CAF50; 
                                 color: white; border: none; border-radius: 5px; 
                                 cursor: pointer;">
                        Download Paper
                    </button>
                </a>
            </div>
            """
            title.value = paper_data["title"]
            explanation.value = paper_data["explanation"]
            download_html.value = init_download_link

        return interface
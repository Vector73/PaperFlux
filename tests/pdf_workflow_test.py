import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pathlib import Path

GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

class PaperAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

    def analyze_paper(self, pdf_path: str) -> str:
        """
        Process entire PDF with images using Gemini's native PDF handling
        Returns detailed technical analysis including visual elements
        """
        try:
            abs_path = Path(pdf_path).absolute()
            print(f"Looking for PDF at: {abs_path}")
            
            if not abs_path.exists():
                available_files = list(abs_path.parent.glob('*'))
                print(f"Available files: {available_files}")
                return f"File not found: {abs_path}"

            uploaded_file = genai.upload_file(str(abs_path))

            uploaded_file = genai.upload_file(pdf_path)
            
            prompt = f"""Analyze this research paper thoroughly, considering both text and visual elements:
            Provide in depth explanation with all core mathematical concepts and intuition behind them.

            1. Paper Structure Analysis:
               - Identify key sections (Abstract, Methodology, Results, etc.)
               - Map the paper's argument flow

            2. Technical Content:
               - Explain core innovations with equations/examples
               - Analyze diagrams/figures and their significance
               - Extract key algorithms/pseudocode

            3. Critical Evaluation:
               - Strengths/weaknesses of methodology
               - Compare with cited works
               - Suggest improvements

            4. Visual Element Analysis:
               - Describe important figures/diagrams
               - Explain visual data representations
               - Connect images to textual content

            Format output in Markdown with these sections:
            # Paper Title
            ## Core Contribution
            ## Technical Breakdown
            ## Visual Analysis
            ## Critical Assessment
            ## Potential Applications
            """

            response = self.model.generate_content(
                [prompt, uploaded_file],
                safety_settings=self.safety_settings,
                generation_config={"temperature": 0.2}
            )
            
            genai.delete_file(uploaded_file.name)
            return response.text

        except Exception as e:
            return f"Analysis failed: {str(e)}"

if __name__ == "__main__":
    analyzer = PaperAnalyzer()
    
    paper_path = r"papers/test_pdf.pdf"
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Path exists: {Path(paper_path).exists()}")
    
    analysis = analyzer.analyze_paper(paper_path)
    print(analysis)
    
    with open("full_analysis.md", "w") as f:
        f.write(analysis)
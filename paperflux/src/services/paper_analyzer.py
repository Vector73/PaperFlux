import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from src.config.settings import GEMINI_API_KEY

class PaperAnalyzer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    def analyze_paper(self, pdf_path: str) -> str:
        uploaded_file = genai.upload_file(pdf_path)
        prompt = """Analyze this research paper thoroughly and provide:

        # Paper Title
        ## Core Contribution
        ## Technical Breakdown
        - Detailed mathematical concepts and intuition with in depth explanation
        - Key algorithms and methodologies
        ## Visual Analysis
        ## Critical Assessment
        ## Potential Applications
        
        Include detailed mathematical expressions and thorough explanations."""

        response = self.model.generate_content(
            [prompt, uploaded_file],
            safety_settings=self.safety_settings,
            generation_config={"temperature": 0.2},
        )

        genai.delete_file(uploaded_file.name)
        return response.text

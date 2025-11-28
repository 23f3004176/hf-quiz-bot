import os
import time
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from smolagents import CodeAgent, LiteLLMModel
from tools import visit_page_and_extract_text
import litellm

app = FastAPI()

# --- CONFIGURATION (SECURE) ---
STUDENT_EMAIL = os.environ.get("STUDENT_EMAIL", "23f3004176@ds.study.iitm.ac.in")
STUDENT_SECRET = os.environ.get("STUDENT_SECRET")

if not STUDENT_SECRET:
    raise ValueError("CRITICAL: STUDENT_SECRET is missing. Add it to Hugging Face Settings.")

# --- MODEL SETUP ---
# Using Gemini 2.0 Flash Lite for speed and logic.
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash-lite", 
    temperature=0.1, # Keep it logical, not creative
    api_key=os.environ.get("GEMINI_API_KEY") 
)

# --- AGENT SETUP ---
# Authorized for Sourcing, Analysis, Visualization, and Scraping
authorized_imports = [
    "pandas", "numpy", "json", "re", "math", "requests", "bs4", "io",
    "matplotlib", "seaborn", "sklearn", "scipy", "pypdf", "openpyxl", 
    "random", "statistics", "lxml", "time", "datetime"
]

agent = CodeAgent(
    tools=[visit_page_and_extract_text],
    model=model,
    additional_authorized_imports=authorized_imports
)

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

def solve_quiz_loop(start_url: str):
    current_url = start_url
    
    # Increased loop limit to handle multi-step chains
    for i in range(12): 
        print(f"--- Step {i+1}: Processing {current_url} ---")
        
        prompt = f"""
        You are an Expert Quiz Solver.
        
        GOAL: Solve the quiz at {current_url}
        
        ---------------------------------------------------
        PHASE 1: ANALYZE & SOLVE
        1. READ the page using `visit_page_and_extract_text(url)`.
        2. DETERMINE the task type and SOLVE it:
        
           [TYPE A: SIMPLE INSTRUCTION] (Priority for Demo)
           - Trigger: Page contains a JSON block with `"answer": "..."`.
           - Action: Extract that exact answer text (e.g. "anything you want", "42").
           
           [TYPE B: DATA ANALYSIS / FILES]
           - Trigger: Mentions "CSV", "Excel", "PDF", or "Download".
           - Action: 
             a. Find the file link (href) using BeautifulSoup.
             b. Download it with `requests.get()`.
             c. Read with `pandas` (CSV/Excel) or `pypdf` (PDF).
             d. Perform the requested math (Sum, Filter, Regression, etc.).
             
           [TYPE C: SOURCING / API]
           - Trigger: "Fetch data from API", "Source from...".
           - Action: Use `requests.get(api_url, headers=...)` to get data and parse JSON.
           
           [TYPE D: VISUALIZATION]
           - Trigger: "Generate a chart", "Plot".
           - Action: Use `matplotlib` to create the plot if asked, or calculate data points.
           
           [TYPE E: SCRAPING]
           - Trigger: "Find the email", "Count items", "Secret code is...".
           - Action: Scrape the text directly from the page content.
        
        ---------------------------------------------------
        PHASE 2: SUBMISSION
        1. FIND the Submission URL (look for "Post your answer to...").
        2. PREPARE the JSON payload:
        {{
            "email": "{STUDENT_EMAIL}",
            "secret": "{STUDENT_SECRET}",
            "url": "{current_url}",        
            "answer": <THE_RESULT>
        }}
        
        3. SUBMIT using `requests.post(submission_url, json=payload)`.
        4. CHECK RESPONSE: If `{{ "correct": true, "url": "..." }}`, return the new URL string.
        """
        
        try:
            max_retries = 3
            result = None
            
            for attempt in range(max_retries):
                try:
                    result = agent.run(prompt)
                    break 
                except Exception as e:
                    if "503" in str(e) or "Overloaded" in str(e):
                        print(f"⚠️ Google API Overloaded. Retrying...")
                        time.sleep(2)
                    else:
                        # Log error but don't crash loop immediately if it's retryable
                        print(f"⚠️ Agent Error: {e}")
                        if attempt == max_retries - 1:
                            raise e
            
            print(f"Agent Result: {result}")

            # Recursion Logic
            result_str = str(result)
            if "http" in result_str and "tds-llm-analysis" in result_str:
                import re
                urls = re.findall(r'https?://[^\s"\']+', result_str)
                if urls:
                    # Find a URL that isn't the current one to avoid loops
                    next_url = None
                    for u in urls:
                        if u != current_url and "submit" not in u:
                            next_url = u
                            break
                    
                    if next_url:
                        current_url = next_url
                        continue
            
            print("Quiz flow ended or completed.")
            break
                
        except Exception as e:
            print(f"❌ Error in loop: {e}")
            break

@app.post("/run")
async def run_quiz(request: QuizRequest, background_tasks: BackgroundTasks):
    if request.secret != STUDENT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    background_tasks.add_task(solve_quiz_loop, request.url)
    return {"message": "Universal Agent started", "status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
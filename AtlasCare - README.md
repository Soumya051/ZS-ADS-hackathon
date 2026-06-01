# Project AtlasCare — README

## Setup

**1. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**
A `.env` file is included in the repository with all required keys pre-populated except the Gemini API key. Open `.env` and add your key:
```
GEMINI_API_KEY=your_key_here
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

## Testing the Classifier
The prompt/planner module can be tested directly from the terminal by passing a query string as an argument. This prints the raw Gemini output so you can verify the structure of the classified response before running the full agent.
```bash
python prompt.py "Where is my order ORD-12345?"
```
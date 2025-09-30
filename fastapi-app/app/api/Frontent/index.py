from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
import httpx


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to My API</title>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Quicksand', sans-serif;
                background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                color: #333;
            }

            .card {
                background: white;
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                text-align: center;
                animation: fadeIn 1.2s ease-in-out;
            }

            h1 {
                margin-bottom: 0.5rem;
                font-size: 2rem;
                color: #5a5a5a;
            }

            p {
                margin-top: 0;
                font-size: 1.1rem;
                color: #777;
            }

            a {
                display: inline-block;
                margin-top: 1.5rem;
                padding: 0.75rem 1.5rem;
                background: #6c63ff;
                color: white;
                border-radius: 30px;
                text-decoration: none;
                font-weight: 600;
                transition: background 0.3s ease;
            }

            a:hover {
                background: #574b90;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>✨ Welcome to My API ✨</h1>
            <p>Your FastAPI app is running beautifully.</p>
            <a href="/index/form">🚀 Explore API Docs</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/form", response_class=HTMLResponse)
async def advanced_form():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Add New Item</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: #f4f6f8;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .form-container {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.1);
                max-width: 400px;
                width: 100%;
            }
            h2 {
                text-align: center;
                color: #333;
                margin-bottom: 1.5rem;
            }
            label {
                font-weight: 600;
                display: block;
                margin-bottom: 0.5rem;
                margin-top: 1rem;
                color: #444;
            }
            input, textarea {
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 1rem;
                box-sizing: border-box;
                transition: border-color 0.3s;
            }
            input:focus, textarea:focus {
                border-color: #6c63ff;
                outline: none;
            }
            button {
                margin-top: 1.5rem;
                background: #6c63ff;
                color: white;
                border: none;
                width: 100%;
                padding: 0.75rem;
                border-radius: 6px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.3s ease;
            }
            button:hover {
                background: #574b90;
            }
            .footer {
                text-align: center;
                margin-top: 1rem;
            }
            .footer a {
                color: #6c63ff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>📝 Add New Item</h2>
            <form method="post" action="/index/form-submit">
                <label for="id">Item ID</label>
                <input type="number" name="id" required />

                <label for="name">Name</label>
                <input type="text" name="name" required />

                <label for="description">Description</label>
                <textarea name="description" rows="3" placeholder="Optional..."></textarea>

                <button type="submit">Submit</button>
            </form>
            <div class="footer">
                <a href="/docs">📘 View API Docs</a>
                <a href="/api/v1"> 📘 GET ALL API </a>
            </div>
        </div>
    </body>
    </html>
    """)

@router.post("/form-submit", response_class=HTMLResponse)
async def submit_item(id: int = Form(...), name: str = Form(...), description: str = Form(None)):
    data = {"id": id, "name": name, "description": description}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://host.docker.internal:9000/api/v1/", json=data)
        
        print("Response status:", response.status_code)
        print("Response text:", response.text)

        if response.status_code ==201:
            return HTMLResponse(content=f"""
            <html>
                <head>
                    <title>Success</title>
                </head>
                <body style="font-family: Inter, sans-serif; text-align: center; padding-top: 80px;">
                    <h2 style="color: green;">✅ Item Created!</h2>
                    <p><strong>ID:</strong> {id}</p>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Description:</strong> {description or "N/A"}</p>
                    <a href="/index/form" style="display: inline-block; margin-top: 20px; color: #6c63ff;">Add Another Item</a>
                </body>
            </html>
            """)
        else:
            # Attempt to parse JSON error; fallback to raw text if it fails
            try:
                error_detail = response.json().get("detail", "Something went wrong")
            except Exception as e:
                print("Error parsing JSON:", e)
                error_detail = response.text or "Something went wrong"

            return HTMLResponse(content=f"""
            <html>
                <head><title>Error</title></head>
                <body style="font-family: Inter, sans-serif; text-align: center; padding-top: 80px;">
                    <h2 style="color: red;">❌ Error</h2>
                    <p>{error_detail}</p>
                    <a href="/index/form" style="display: inline-block; margin-top: 20px; color: #6c63ff;">Try Again</a>
                </body>
            </html>
            """, status_code=response.status_code)

    except httpx.ConnectError as e:
        print("❌ Connection error:", e)
        return HTMLResponse(content=f"""
        <html>
            <head><title>API Connection Error</title></head>
            <body style="font-family: Inter, sans-serif; text-align: center; padding-top: 80px;">
                <h2 style="color: red;">🔌 Could not connect to the API</h2>
                <p>{str(e)}</p>
                <a href="/index/form" style="display: inline-block; margin-top: 20px; color: #6c63ff;">Try Again</a>
            </body>
        </html>
        """, status_code=500)
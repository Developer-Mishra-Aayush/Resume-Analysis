from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import Registration, Company  # adjust if your app name is different
from hr_dashboard.models import JobDescriptions  # adjust if your app name is different
from .models import Resume
import pymupdf4llm
from groq import Groq
import json
from decouple import config

import json
import pymupdf4llm
from groq import Groq
from django.conf import settings

def extract_text_from_resume_and_analyze(path, jd_id):
    # 1. Fetch JD data from your Django models
    try:
        jd_instance = JobDescriptions.objects.get(id=jd_id)
        jd_description = jd_instance.description
        # Clean the list to ensure no extra whitespace
        required_skills = [s.strip() for s in jd_instance.required_skills.split(',')]
    except JobDescriptions.DoesNotExist:
        print(f"Error: JD with id {jd_id} not found.")
        return {"is_resume": False, "error": "JD not found"}

    # 2. Convert PDF to Markdown (using the layout-aware settings)
    # Using header/footer=False to avoid noise like page numbers
    md = pymupdf4llm.to_markdown(path, header=False, footer=False)

    # 3. Construct the optimized prompt

    output_format = {
        "is_resume": True,
        "score": 0,
        "match_level": "",
        "date_ranges": [],
        "total_experience": "",
        "skills": {
            "matched": [],
            "missing": [],
            "extra": []
        },
        "project_categories": [],
        "suggestions": [
            {"level": "High", "title": "", "desc": ""},
            {"level": "Medium", "title": "", "desc": ""},
            {"level": "Low", "title": "", "desc": ""}
        ]
    }

    prompt = f"""
    SYSTEM ROLE:
    You are an Expert Technical Recruiter and ATS system.

    GOAL:
    Analyze the Resume against the Job Description and return STRICT JSON output.

    INPUT:
    1. Target Required Skills: {required_skills}
    2. Job Description: {jd_description}
    3. Resume (Markdown):
    {md}

    ========================
    ANALYSIS RULES
    ========================

    1. SKILL ANALYSIS:
    - Extract skills by comparing "Target Required Skills" with resume content
    - Return SHORT skill names only (1–3 words max)
    - NO sentences or explanations
    - Example: "Python", "Django", "REST API"
    - Categorize into:
    - matched
    - missing
    - extra

    ------------------------

    2. EXPERIENCE EXTRACTION:

    - Extract date ranges ONLY from "Work Experience" or similar sections
    - Use markdown headings (##, ###) to identify:
    "Experience", "Work Experience", "Professional Experience"

    STRICTLY IGNORE dates from:
    - Projects
    - Education
    - Certifications
    - Any other section

    ONLY include:
    - Full-time roles
    - Internships
    - Professional work

    IGNORE:
    - Project-based dates
    - Freelance work unless clearly marked as experience

    FORMAT:
    - "MMM YYYY - MMM YYYY"
    - "MMM YYYY - Present"

    EXAMPLE:
    ["Jan 2022 - Mar 2023", "Apr 2023 - Present"]

    - If no experience found → return []

    ------------------------

    3. TOTAL EXPERIENCE:
    - Calculate total experience ONLY from extracted ranges
    - Format: "X years Y months"

    ------------------------

    4. PROJECT CATEGORIES:
    - Return top 3–4 domains
    - Example: "Web Development", "Database Design"

    ------------------------

    5. SCORING:
    - Skill Match → 50%
    - Experience → 30%
    - Projects → 20%
    - Score must be 0–100

    ------------------------

    6. MATCH LEVEL:
    - 80–100 → Good Match
    - 60–79 → Moderate Match
    - <60 → Low Match

    ------------------------

    7. SUGGESTIONS:
    - EXACTLY 3 suggestions
    - Levels: High, Medium, Low
    - Short + actionable

    ========================
    OUTPUT FORMAT (STRICT JSON ONLY)
    ========================

    {json.dumps(output_format, indent=4)}

    ========================
    IMPORTANT RULES
    ========================

    - Return ONLY JSON
    - No markdown, no explanation
    - No extra text before/after JSON
    - Do NOT extract project dates as experience
    - If input is not a resume → return:
    {{"is_resume": false}}
    """

    try:
        client = Groq(api_key=config('API_KEY'))
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            temperature=0.0, # Keep it deterministic for consistent scoring
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        data = json.loads(result)

        if not data.get("is_resume"):
            return data

        
        # Clean up by removing the raw dates from final response if not needed for UI
        # data.pop("date_ranges", None) 

        return data
        print("Final Result is : ", data)
    except Exception as e:
        print("Error in extract_text_from_resume_and_analyze:", e)
        return {"is_resume": False, "error": str(e)}
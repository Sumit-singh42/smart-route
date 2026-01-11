import os

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Research Engine Architecture</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #1e293b;
            --accent: #f59e0b;
            --bg: #f8fafc;
            --card-bg: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #334155;
            background-color: var(--bg);
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        header {
            background: linear-gradient(135deg, var(--primary), #1d4ed8);
            color: white;
            padding: 60px 20px;
            text-align: center;
            border-radius: 0 0 20px 20px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        h1 { margin: 0; font-size: 2.5rem; font-weight: 700; }
        .subtitle { opacity: 0.9; font-size: 1.1rem; margin-top: 10px; }
        
        .section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
        }
        h2 {
            color: var(--secondary);
            border-bottom: 2px solid var(--primary);
            padding-bottom: 10px;
            margin-top: 0;
        }
        h3 { color: var(--primary); margin-top: 25px; }
        
        .stage-card {
            background: #f1f5f9;
            border-left: 4px solid var(--primary);
            padding: 20px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }
        .stage-title { font-weight: bold; color: var(--secondary); font-size: 1.1rem; }
        .stage-role { color: var(--primary); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
        
        .diagram-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 20px 0;
            overflow-x: auto;
        }

        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .tech-item {
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        .tech-head { font-weight: bold; color: var(--secondary); margin-bottom: 5px; display: block;}
        
        .footer { text-align: center; color: #64748b; margin-top: 50px; font-size: 0.9rem; }
    </style>
</head>
<body>

    <header>
        <h1>Automated Evidence-Based Research Engine</h1>
        <div class="subtitle">System Pipeline & Architecture Documentation</div>
    </header>

    <div class="container">

        <div class="section">
            <h2>1. System Overview</h2>
            <p>
                The system operates as a <strong>deterministic, multi-stage pipeline</strong> handled by specialized agents. 
                Unlike standard large language models (LLMs) that attempt to answer prompts in a single pass, this architecture 
                enforces a strict, step-by-step workflow. This modular design ensures <strong>traceability</strong> (every claim is linked to a source), 
                <strong>explainability</strong> (the reasoning path is visible), and <strong>quality control</strong> (bad data is rejected).
            </p>
        </div>

        <div class="section">
            <h2>2. Visual Workflow Pipeline</h2>
            <p>The following diagram illustrates the circular flow of information, including the critical feedback loop triggered by the Reviewer Agent.</p>
            <div class="diagram-container">
                <div class="mermaid">
                    graph TD
                        Goal[User Research Goal] --> S1
                        
                        subgraph "Phase 1: Planning & Discovery"
                        S1[Stage 1: Topic Decomposition<br/><i>Research Planning Agent</i>] --> S2
                        S2[Stage 2: Document Discovery<br/><i>Web & Academic Search</i>] --> S3
                        end

                        subgraph "Phase 2: Analysis & Verification"
                        S3[Stage 3: Content Analysis<br/><i>Reading & Extraction</i>] --> S4
                        S4[Stage 4: Source Scoring<br/><i>Credibility Evaluation</i>] --> S5
                        S5[Stage 5: Knowledge Base<br/><i>Filtered Evidence Store</i>] --> S6
                        end

                        subgraph "Phase 3: Synthesis & Quality"
                        S6[Stage 6: Structured Synthesis<br/><i>Outline & Claim Mapping</i>] --> S7
                        S7[Stage 7: Insight Generation<br/><i>Standards-Compliant Output</i>] --> S8
                        S8[Stage 8: Reviewer Agent<br/><i>Quality Control Loop</i>]
                        end

                        S8 -- Pass --> Final[Final Output<br/><i>Audit-Ready Report</i>]
                        S8 -- Fail --> Feedback[Feedback Loop<br/><i>Regenerate Plan</i>]
                        Feedback -.-> S1

                        style Goal fill:#2563eb,color:#fff
                        style Final fill:#10b981,color:#fff
                        style Feedback fill:#f59e0b,color:#fff
                        style S8 fill:#1e293b,color:#fff
                </div>
            </div>
        </div>

        <div class="section">
            <h2>3. Detailed Stage Breakdown</h2>
            
            <h3>Phase 1: Research Planning</h3>
            <div class="stage-card">
                <div class="stage-role">Stage 1: The Planner</div>
                <div class="stage-title">Topic Decomposition</div>
                <p>The system receives a high-level goal and uses the LLM to decompose it into granular sub-questions, specific search keywords, and constraints. This prevents vague searches and sets a strict scope.</p>
            </div>
            
            <div class="stage-card">
                <div class="stage-role">Stage 2: The Hunter</div>
                <div class="stage-title">Evidence Discovery</div>
                <p>Using the plan, the system queries targeted sources (Academic papers, Trusted Web). It employs "controlled search" to filter out noise before ingestion.</p>
            </div>

            <h3>Phase 2: Verification & Storage</h3>
            <div class="stage-card">
                <div class="stage-role">Stage 3: The Reader</div>
                <div class="stage-title">Content Analysis</div>
                <p>Raw documents (PDFs, HTML) are parsed. The agent extracts core claims, methodologies, and data, normalizing unstructured text into a standard format.</p>
            </div>

            <div class="stage-card">
                <div class="stage-role">Stage 4: The Gatekeeper</div>
                <div class="stage-title">Credibility Scoring</div>
                <p>Every source is scored on Authority, Relevance, and Citation worthiness. Low-quality sources are discarded here to prevent "Garbage In, Garbage Out".</p>
            </div>

            <div class="stage-card">
                <div class="stage-role">Stage 5: The Memory</div>
                <div class="stage-title">Knowledge Base Creation</div>
                <p>Verified evidence is compiled into a structured store. Each claim is physically linked to its source, enabling the "citation" feature in the final output.</p>
            </div>

            <h3>Phase 3: Synthesis & Output</h3>
            <div class="stage-card">
                <div class="stage-role">Stage 6: The Architect</div>
                <div class="stage-title">Structured Synthesis</div>
                <p>The system maps evidence to arguments. <b>Crucially, no creative writing occurs here.</b> It only organizes existing facts into a logical skeleton.</p>
            </div>

            <div class="stage-card">
                <div class="stage-role">Stage 7: The Writer</div>
                <div class="stage-title">Insight Generation</div>
                <p>The skeleton is converted into the final format (Technical Report, Literature Review) following professional styling standards.</p>
            </div>

            <div class="stage-card">
                <div class="stage-role">Stage 8: The Auditor</div>
                <div class="stage-title">Automated Peer Review</div>
                <p>A separate agent reviews the draft for logical consistency and evidence gaps. If the score is low, it triggers the <b>Feedback Loop</b> to regenerate the content.</p>
            </div>
        </div>

        <div class="section">
            <h2>4. Technology Stack</h2>
            <div class="tech-grid">
                <div class="tech-item">
                    <span class="tech-head">Core Runtime</span>
                    Python 3.8+ (Scalability & Prototyping)
                </div>
                <div class="tech-item">
                    <span class="tech-head">Reasoning Engine</span>
                    ChatGPT API (Logic & Evaluation), Gemini/Groq (Speed Fallback)
                </div>
                <div class="tech-item">
                    <span class="tech-head">Search & Retrieval</span>
                    Google Programmable Search, BeautifulSoup, PDF Parsers
                </div>
                <div class="tech-item">
                    <span class="tech-head">Knowledge Storage</span>
                    Vector DBs (FAISS / ChromaDB) for persistent memory
                </div>
                <div class="tech-item">
                    <span class="tech-head">Security</span>
                    dotenv for API Key Management
                </div>
                <div class="tech-item">
                    <span class="tech-head">Output Formats</span>
                    Markdown, PDF, DOCX, JSON
                </div>
            </div>
        </div>

        <div class="footer">
            Generated from Document Source: Automated Evidence-Based Research & Insight Engine
        </div>

    </div>

    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
"""

# Write the file
file_name = "Research_Pipeline_Report.html"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated '{file_name}'. Open this file in your web browser to view the visual report.")
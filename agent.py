import os
import logging
import datetime
import google.cloud.logging
from google.cloud import datastore
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from mcp.server.fastmcp import FastMCP 

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# ================= 1. SETUP =================

try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-1.5-flash")

# ================= 2. DATABASE =================
DB_ID = "genshreya"
db = datastore.Client()
mcp = FastMCP("MiniJarvisTools")

# ================= 3. TOOLS =================

@mcp.tool()
def add_task(title: str) -> str:
    """Add a new task."""
    try:
        key = db.key('Task')
        task = datastore.Entity(key=key)
        task.update({
            'title': title,
            'completed': False,
            'created_at': datetime.datetime.now()
        })
        db.put(task)
        return f"✅ Task '{title}' added successfully."
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def list_tasks() -> str:
    """List all tasks."""
    try:
        query = db.query(kind='Task')
        tasks = list(query.fetch())

        if not tasks:
            return "📭 No tasks found."

        result = ["📋 Your Tasks:"]
        for t in tasks:
            status = "✅" if t.get('completed') else "⏳"
            result.append(f"{status} {t.get('title')} (ID: {t.key.id})")

        return "\n".join(result)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def complete_task(task_id: str) -> str:
    """Mark a task as completed."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, task_id)))
        key = db.key('Task', numeric_id)
        task = db.get(key)

        if task:
            task['completed'] = True
            db.put(task)
            return f"✅ Task {numeric_id} completed."

        return "❌ Task not found."
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Save a note."""
    try:
        key = db.key('Note')
        note = datastore.Entity(key=key)
        note.update({
            'title': title,
            'content': content,
            'created_at': datetime.datetime.now()
        })
        db.put(note)
        return f"📝 Note '{title}' saved."
    except Exception as e:
        return f"Error: {str(e)}"


# ================= 4. AGENTS =================

def save_prompt(tool_context: ToolContext, prompt: str):
    tool_context.state["PROMPT"] = prompt
    return {"status": "saved"}


# 🎯 Main Instruction (Jarvis Personality)
def jarvis_instruction(ctx):
    user_prompt = ctx.state.get("PROMPT", "Hello")

    return f"""
You are Mini Jarvis 🤖, a smart personal productivity assistant.

Your job:
- Help manage tasks
- Save notes
- Track productivity
- Be friendly and helpful

User Request:
{user_prompt}

Instructions:
- If user wants to add task → use add_task
- If user asks for tasks → use list_tasks
- If user wants to complete task → use complete_task
- If user wants to save notes → use add_note
- If user asks to plan day → suggest a simple schedule

Always respond clearly and helpfully.
"""


# Root instruction
def root_instruction(ctx):
    raw_input = ctx.state.get("user_input", "Hello")
    return f"""
1. Save this input using 'save_prompt': {raw_input}
2. Then pass control to the 'workflow'
"""


# 🤖 Main Agent
jarvis_agent = Agent(
    name="mini_jarvis_agent",
    model=model_name,
    instruction=jarvis_instruction,
    tools=[add_task, list_tasks, complete_task, add_note]
)

# 🔄 Workflow
workflow = SequentialAgent(
    name="productivity_workflow",
    sub_agents=[jarvis_agent]
)

# 🚀 Root Agent
root_agent = Agent(
    name="root_agent",
    model=model_name,
    instruction=root_instruction,
    tools=[save_prompt],
    sub_agents=[workflow]
)

# ================= 5. API =================

app = FastAPI()

class UserRequest(BaseModel):
    prompt: str


@app.post("/api/v1/jarvis/chat")
async def chat(request: UserRequest):
    try:
        final_reply = ""

        async for event in root_agent.run_async({"user_input": request.prompt}):
            if hasattr(event, 'text') and event.text:
                final_reply = event.text

        return {
            "status": "success",
            "reply": final_reply if final_reply else "Done."
        }

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================= 6. RUN =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
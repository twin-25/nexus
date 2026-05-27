import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from anthropic import Anthropic
import json
from bank.tools import analyze_jd, draft_section, score_match, get_entry, get_skills
from bank.services import search_bank

client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))


SYSTEM_PROMPT = """You are an intelligent resume assistant helping a job seeker tailor their resume.

When a user pastes a job description:
1. Immediately analyze it using analyze_jd
2. Search the experience bank using search_bank
3. Tell the user what you found and propose what to include
4. Ask for confirmation before drafting

Never ask if the user is a recruiter or candidate — you are always helping the job seeker.
Never ask if they have an experience bank — it already exists.
Always take action first, ask questions only when genuinely stuck.

You have access to these tools:
- analyze_jd: Extract role, skills, domain and keywords from a job description
- search_bank: Search the experience bank for relevant entries
- get_entry: Get full details of a specific entry by title
- get_skills: Get all skills from the experience bank
- draft_section: Draft a resume section based on entries and job description
- score_match: Score how well the experience matches the job description

Rules:
- Never hallucinate experience — only use what's in the bank
- Be conversational and explain your reasoning
- Always show which tools you're calling
"""


tools = [
  {
    "name": "analyze_jd",
    "description": "analyzes the job description and extract role, seniority, domain, required_skills, nice_to_have, and keywords from the job description",
    "input_schema":{
      "type":"object",
      "properties":{
        "job_description":{
          "type":"string",
          "description":"the full job description text",
        },
        
      },
      "required":["job_description"]
    }
  },
  {
    "name": "draft_section",
    "description": "Based on the job description and experience,  writes the required section of the resume ",
    "input_schema":{
      "type":"object",
      "properties":{
        "entries": {
          "type": "array",
          "description": "list of relevant entries from search_bank"
        },
        "job_description":{
          "type":"string",
          "description":"the full job description text",
        },
        "section":{
          "type":"string",
          "description":"the required section of the resume that needed to be written",
        },
      },
      "required":["entries", "job_description", "section"]
    }
  },

  {
    "name": "score_match",
    "description": "Score how well the experience matches the job description",
    "input_schema":{
      "type":"object",
      "properties":{
        "job_description":{
          "type":"string",
          "description":"the full job description text",
        },
        "draft":{
          "type":"string",
          "description":"drafted resume content to score",
        },
      },
      "required":["job_description", "draft"]
    }
  },

  {
    "name": "get_entry",
    "description": "get full details of the entries based on the specific titles",
    "input_schema":{
      "type":"object",
      "properties":{
        "title": {
        "type": "string",
        "description": "title of the entry to retrieve"
      }
      },
      "required":["title"],
    }
  },

  {
    "name": "get_skills",
    "description": "get all skills of the user",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
},

{
    "name": "search_bank",
    "description": "Search the experience bank for relevant entries based on a query",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "search query to find relevant experience entries"
            }
        },
        "required": ["query"]
    }
}
  
]

def execute_tool(tool_name, tool_input, session):
    if tool_name == "search_bank":
        result = search_bank(tool_input["query"])
        entries = [{"title": e.title, "raw": e.raw, "context": e.context} for e in result]
        session["relevant_entries"] = entries
        return entries

    elif tool_name == "analyze_jd":
        result = analyze_jd(tool_input["job_description"])
        session["jd_analysis"] = result
        session["jd"] = tool_input["job_description"]
        return result

    elif tool_name == "get_skills":
        result = get_skills()
        skills = [{"name": s.name, "category": s.category} for s in result]
        return skills

    elif tool_name == "get_entry":
        result = get_entry(tool_input["title"])
        return {"title": result.title, "raw": result.raw, "context": result.context}

    elif tool_name == "draft_section":
        result = draft_section(
            tool_input["entries"],
            tool_input["job_description"],
            tool_input["section"]
        )
        session["drafted_sections"][tool_input["section"]] = result
        return result

    elif tool_name == "score_match":
      result = score_match(
          tool_input.get("jd") or tool_input.get("job_description"),
          tool_input["draft"]
      )
      session["score"] = result
      return result

    else:
        return {"error": f"Unknown tool: {tool_name}"}
  


        
        
def run_agent():
    conversation_history = []
    session = {
        "jd": None,
        "jd_analysis": None,
        "relevant_entries": [],
        "drafted_sections": {},
        "score": None
    }
    
    print("Resume Agent ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "quit":
            break
            
        if not user_input:
            continue

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        while True:
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=conversation_history
            )
            
            if response.stop_reason == "tool_use":
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        print(f"\n[Agent calling: {block.name}]")
                        result = execute_tool(block.name, block.input, session)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, default=str)
                        })

                conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

            elif response.stop_reason == "end_turn":
                final_response = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_response += block.text
                
                print(f"\nAgent: {final_response}\n")
                
                conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                break


if __name__ == "__main__":
    run_agent()
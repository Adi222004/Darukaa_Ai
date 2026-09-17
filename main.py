from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from reasoning.conversation import ConversationManager
from reasoning.recommender import generate_recommendations
from rag.retriever import retrieve

app = FastAPI(title="Darukaa Watershed AI")

conversations: Dict[str, ConversationManager] = {}

class QueryRequest(BaseModel):
    user_id: str
    message: str
    structured_data: Optional[Dict[str, Any]] = None

@app.post("/chat")
async def chat(request: QueryRequest):
    if request.user_id not in conversations:
        conversations[request.user_id] = ConversationManager()

    cm = conversations[request.user_id]
    cm.add_message("user", request.message)

    if request.structured_data:
        cm.update_slots(request.structured_data)

    missing = cm.get_missing_slots()
    if missing:
        question = f"I can help with that. To give you a scientific recommendation, I need a bit more data. Can you provide: {', '.join(missing)}?"
        cm.add_message("assistant", question)
        return {"response": question, "type": "clarification", "missing_slots": missing}

    recs = generate_recommendations(cm.slots)

    rec_names = " ".join([r['recommendation'] for r in recs]) if recs else ""
    docs = retrieve(f"{request.message} {rec_names}".strip())

    response_text = "Based on your watershed data, here are my recommendations:\n\n"

    if not recs:
        response_text += "No specific recommendations triggered. Try adjusting the sidebar values."

    for rec in recs:
        response_text += f"**{rec['recommendation']}**\n"
        response_text += f"- *Why:* {rec['why']}\n"
        response_text += f"- *Metrics improved:* {', '.join(rec['metrics_improved'])}\n"
        response_text += f"- *Time horizon:* {rec['time_horizon']}\n"
        response_text += f"- *Confidence:* {rec['confidence']}\n"
        if rec.get('evidence'):
            response_text += "- *Evidence:*\n"
            for ev in rec['evidence']:
                response_text += f"  - {ev['source']} ({ev['year']}) - [Link]({ev['url']})\n"
        response_text += "\n"

    if docs:
        response_text += "---\n**📚 Knowledge Retrieved from Vector DB (RAG):**\n"
        for i, d in enumerate(docs[:1]):
            snippet = d['content'][:250].replace('\n', ' ')
            response_text += f"{i+1}. *{snippet}...*\n"

    cm.add_message("assistant", response_text)
    return {"response": response_text, "recommendations": recs, "retrieved_docs_count": len(docs)}
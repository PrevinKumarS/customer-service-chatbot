import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from schema import ChatResponse

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class BankingChatbot:
    def __init__(self):
        # Use relative pathing based on current file location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.kb_path = os.path.join(base_dir, "knowledgebase")
        self.kb_content = self._load_knowledgebase()

    def _load_knowledgebase(self) -> str:
        """Loads all JSON files from knowledgebase folder into a string context."""
        context_parts = []
        if not os.path.exists(self.kb_path):
            return "Knowledgebase directory not found."

        for filename in os.listdir(self.kb_path):
            if filename.endswith(".json"):
                try:
                    path = os.path.join(self.kb_path, filename)
                    with open(path, "r") as f:
                        data = json.load(f)
                        context_parts.append(f"Source {filename}:\n{json.dumps(data)}")
                except Exception as e:
                    context_parts.append(f"Error loading {filename}: {str(e)}")
        
        return "\n\n".join(context_parts)

    def _get_system_prompt(self):
        return f"""
        You are 'SecureBank Assistant', a professional AI customer service representative for SecureBank.
        
        GUIDELINES:
        1. Use the provided Knowledgebase to answer queries. 
        2. Use Chain-of-Thought: Reason internally about the intent and facts before generating the final response.
        3. Response Tone: Helpful, concise, and professional.
        4. Scope: Only answer banking-related questions. Decline off-topic queries politely.
        5. Formatting: You MUST return a valid JSON object matching the requested schema.

        KNOWLEDGEBASE:
        {self.kb_content}

        FEW-SHOT EXAMPLES:
        User: "What's the rate for a 1 year FD?"
        Output JSON: {{
            "turn": 1,
            "user_message": "What's the rate for a 1 year FD?",
            "intent": "account_inquiry",
            "confidence": "High",
            "urgency": "Low",
            "sentiment": "Neutral",
            "escalation_required": false,
            "facts_used": 1,
            "advisor_response": "Our Fixed Deposit rate for a 1-2 year tenure is 7.10% p.a. Senior citizens get an additional 0.50%."
        }}
        """

    def generate_response(self, user_input: str, history: List[Dict]) -> ChatResponse:
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        
        # Add conversation history
        for h in history[-5:]: # Keep last 5 exchanges
            messages.append({"role": "user", "content": h["user"]})
            messages.append({"role": "assistant", "content": h["bot"]})
        
        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13", # Or gpt-3.5-turbo
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            raw_json = response.choices[0].message.content
            # Validate against Pydantic schema
            validated_data = ChatResponse.model_validate_json(raw_json)
            return validated_data
        except Exception as e:
            # Fallback for API or validation errors
            return ChatResponse(
                turn=len(history) + 1,
                user_message=user_input,
                intent="error",
                confidence="Low",
                urgency="Medium",
                sentiment="Neutral",
                advisor_response="I apologize, but I encountered a technical issue processing your request. Please try again or contact support at 1800-XXX-XXXX.",
                notes=f"Error: {str(e)}"
            )
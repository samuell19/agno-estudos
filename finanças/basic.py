from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat
from fastapi.responses import HTMLResponse

basic_agent = Agent(
    name="Basic Agent",
    agent_id="basic_agent",
    model=OpenAIChat(id="gpt-4o"), 
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
)

fastapi_app = FastAPIApp(
    agents=[basic_agent],
    name="Basic Agent",
    app_id="basic_agent",
    description="A basic agent that can answer questions and help with tasks.",
)

app = fastapi_app.get_app()


@app.get("/", response_class=HTMLResponse)
async def get_interface():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Basic Agent</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            #chat { height: 300px; border: 1px solid #ccc; padding: 10px; overflow-y: auto; margin-bottom: 10px; }
            #input { width: 80%; padding: 10px; }
            #send { padding: 10px 20px; }
            .user { text-align: right; color: blue; }
            .agent { text-align: left; color: green; }
        </style>
    </head>
    <body>
        <h1>🤖 Basic Agent</h1>
        <div id="chat"></div>
        <input type="text" id="input" placeholder="Digite sua mensagem..." onkeypress="if(event.key==='Enter') send()">
        <button id="send" onclick="send()">Enviar</button>
        
        <script>
            function addMessage(msg, isUser) {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = isUser ? 'user' : 'agent';
                div.innerHTML = (isUser ? 'Você: ' : 'Agent: ') + msg;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }
            
            async function send() {
                const input = document.getElementById('input');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, true);
                input.value = '';
                
                try {
                    const response = await fetch('/runs?agent_id=basic_agent', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: new URLSearchParams({ message })
                    });
                    const data = await response.json();
                    addMessage(data.content || 'Erro na resposta', false);
                } catch (error) {
                    addMessage('Erro: ' + error.message, false);
                }
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    fastapi_app.serve(app="basic:app", port=8001, reload=True)
from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

# === Configuração do agente ===
chat_agent = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a helpful AI assistant.",
    add_datetime_to_instructions=True,
    markdown=True,
)

agui_app = AGUIApp(
    agent=chat_agent,
    name="Basic AG-UI Agent",
    app_id="basic_agui_agent",
    description="A basic agent that demonstrates AG-UI protocol integration.",
)

app = agui_app.get_app()

# === Rota para a interface simples ===
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AGUI Chat Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px; }
            textarea { width: 100%; height: 80px; margin-bottom: 10px; }
            button { padding: 8px 16px; }
            .messages { border: 1px solid #ccc; padding: 10px; min-height: 200px; margin-bottom: 10px; }
            .user { color: blue; }
            .assistant { color: green; }
        </style>
    </head>
    <body>
        <h2>Chat com AGUI Agent</h2>
        <div class="messages" id="messages"></div>
        <textarea id="input" placeholder="Digite sua mensagem..."></textarea>
        <br>
        <button onclick="sendMessage()">Enviar</button>

        <script>
            async function sendMessage() {
                const input = document.getElementById("input");
                const messagesDiv = document.getElementById("messages");
                const userMessage = input.value.trim();
                if (!userMessage) return;

                // Mostra mensagem do usuário
                messagesDiv.innerHTML += `<div class='user'><b>Você:</b> ${userMessage}</div>`;

                // Envia para a API AGUI
                const res = await fetch("/agui/run", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        threadId: "thread-123",
                        runId: "run-456",
                        state: "{}",
                        messages: [{ id: "msg-1", role: "user", content: userMessage, name: "user" }],
                        tools: [],
                        context: [],
                        forwardedProps: "{}"
                    })
                });

                const data = await res.json();

                // Exibe resposta do agente
                if (data.output && data.output.length > 0) {
                    messagesDiv.innerHTML += `<div class='assistant'><b>Assistente:</b> ${data.output[0].content}</div>`;
                } else {
                    messagesDiv.innerHTML += `<div class='assistant'><b>Assistente:</b> (sem resposta)</div>`;
                }

                input.value = "";
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    agui_app.serve(app="ag:app", port=8000, reload=True)

"""Simple web application (HTML + API)"""

from __future__ import annotations

import json
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pika

host = os.getenv("RABBITMQHOST", "localhost")


def send_to_queue(robot_data: dict) -> None:
    """Publish a payload to the RabbitMQ queue."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host)
    )
    channel = connection.channel()

    channel.queue_declare(queue='robot-queue', durable=True)
    channel.basic_publish(exchange='',routing_key='robot-queue', body=json.dumps(robot_data))
    connection.close()

app = FastAPI()
app.state.click_count = 0


@app.get("/health")
def health() -> dict:
    """Liveness endpoint."""
    return {"message": "Healthy"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    """Render the single-page HTML UI."""
    # Single-file HTML (no templates/static folder) to keep it simple.
    return """
    <!doctype html>
    <html lang="pt-br">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Demo App</title>
        <style>
        :root {
            --bg: #0b1020;
            --card: rgba(255, 255, 255, 0.08);
            --card-border: rgba(255, 255, 255, 0.16);
            --text: rgba(255, 255, 255, 0.92);
            --muted: rgba(255, 255, 255, 0.72);
            --accent: #7c3aed;
            --accent2: #22c55e;
            --shadow: rgba(0, 0, 0, 0.35);
        }

        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100svh;
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto,
            Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
            color: var(--text);
            background:
            radial-gradient(1200px 600px at 10% 10%, rgba(124, 58, 237, 0.40), transparent 55%),
            radial-gradient(900px 500px at 90% 20%, rgba(34, 197, 94, 0.22), transparent 60%),
            radial-gradient(1000px 700px at 50% 95%, rgba(56, 189, 248, 0.12), transparent 55%),
            var(--bg);
            display: grid;
            place-items: center;
            padding: 28px;
        }

        .wrap {
            width: min(980px, 100%);
        }

        .title {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 18px;
        }
        .title h1 {
            margin: 0;
            font-size: clamp(22px, 3.4vw, 36px);
            letter-spacing: -0.02em;
        }
        .title p {
            margin: 0;
            color: var(--muted);
            font-size: 14px;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 18px;
        }

        .card {
            border: 1px solid var(--card-border);
            background: var(--card);
            backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 18px 45px var(--shadow);
            position: relative;
            overflow: hidden;
            cursor: pointer;
            user-select: none;
            transition: transform 140ms ease, border-color 140ms ease;
        }
        .card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.26);
        }
        .card:active {
            transform: translateY(0px) scale(0.99);
        }

        .card .badge {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(0,0,0,0.16);
            color: var(--muted);
            font-size: 12px;
        }

        .card h2 {
            margin: 14px 0 8px;
            font-size: 20px;
            letter-spacing: -0.01em;
        }

        .card .desc {
            margin: 0;
            color: var(--muted);
            line-height: 1.45;
            max-width: 70ch;
        }

        .row {
            display: flex;
            gap: 12px;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-top: 18px;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.16);
            background: rgba(0,0,0,0.14);
            font-size: 13px;
            color: var(--muted);
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            box-shadow: 0 0 0 4px rgba(124,58,237,0.15);
        }

        .cta {
            font-size: 13px;
            color: var(--text);
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.08);
            padding: 10px 12px;
            border-radius: 12px;
        }

        .status {
            margin-top: 14px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
            "Liberation Mono", "Courier New", monospace;
            font-size: 12px;
            color: rgba(255,255,255,0.78);
            white-space: pre-wrap;
            line-height: 1.4;
        }

        .shine {
            position: absolute;
            inset: -120px -80px auto auto;
            width: 260px;
            height: 260px;
            background: radial-gradient(circle at 30% 30%, rgba(124, 58, 237, 0.55), transparent 58%);
            filter: blur(10px);
            transform: rotate(15deg);
            pointer-events: none;
        }
        </style>
    </head>
    <body>
        <main class="wrap">
        <div class="title">
            <div>
            <h1>Mini Web App</h1>
            <p>Clique no card para disparar um POST para a API.</p>
            </div>
            <div class="pill"><span class="dot"></span> FastAPI + HTML inline</div>
        </div>

        <section class="grid">
            <div id="card" class="card" role="button" tabindex="0" aria-label="Disparar POST">
            <div class="shine"></div>
            <span class="badge">POST <strong>/api/click</strong></span>
            <h2>Robô: <span id="robotName">simple-google</span></h2>
            <p class="desc">
                Ao clicar, este card envia um POST com o nome do robô. Depois você pode usar
                esse payload para publicar no RabbitMQ.
            </p>
            <div class="row">
                <span class="pill">Resposta aparece abaixo</span>
                <span class="cta">Clique para testar</span>
            </div>
            <div id="status" class="status">Status: aguardando clique…</div>
            </div>
        </section>
        </main>

        <script>
        const card = document.getElementById("card");
        const statusEl = document.getElementById("status");
        const robotName = "simple-google";
        const robotNameEl = document.getElementById("robotName");
        if (robotNameEl) robotNameEl.textContent = robotName;

        function setStatus(text) {
            statusEl.textContent = text;
        }

        async function send() {
            setStatus("Status: enviando POST…");
            try {
            const res = await fetch("/api/click", {
                method: "POST",
                headers: { "content-type": "application/json" },
                body: JSON.stringify({
                  source: "card",
                  robot: robotName,
                  image: "kevinalmeida/" + robotName + ":latest",
                }),
            });
            const data = await res.json().catch(() => ({}));
            setStatus("Status: " + res.status + "\\n" + JSON.stringify(data, null, 2));
            } catch (err) {
            setStatus("Status: erro\\n" + String(err));
            }
        }

        card.addEventListener("click", send);
        card.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            send();
            }
        });
        </script>
    </body>
    </html>
    """


@app.post("/api/click")
def click(payload: dict) -> dict:
    """Receive a click payload, publish it, and return basic metadata."""
    app.state.click_count += 1
    send_to_queue(payload)
    return {
        "ok": True,
        "message": "POST recebido com sucesso",
        "click_count": app.state.click_count,
        "robot": payload.get("robot"),
        "payload": payload,
    }

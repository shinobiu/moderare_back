from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:

    def gerar_mensagem_checkin(self, dias: int, perdeu: bool, humor) -> str:

        if perdeu:
            contexto = f"O usuário perdeu a sequência e voltou hoje. Ele está no dia {dias}, no momento ele estava se sentindo {humor}."
        else:
            contexto = f"O usuário está mantendo consistência e está no dia {dias}, no momento ele estava se sentindo {humor}."

        prompt = contexto

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": """Você ajuda pessoas a manter disciplina em um app de autocontrole chamado Moderare.
Seu papel é falar como um humano real, não como um coach ou robô motivacional.

Regras:
- Máximo 2 frases
- Português BR
- Nada genérico (evite frases prontas tipo “continue assim”, “você consegue”)
- Nada clínico ou técnico
- Não use tom de coach

Tom:
- Humano, direto e levemente acolhedor
- Pode ser firme quando necessário
- Soa como alguém que entende a situação de verdade

Estilo:
- Fale como se estivesse respondendo uma pessoa específica
- Use variação (não repita estrutura)
- Pode reconhecer esforço ou dificuldade de forma natural
- Evite exagero ou entusiasmo artificial

Objetivo:
Gerar uma mensagem curta que faça sentido pro momento do usuário, baseada no contexto fornecido."""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=60
        )

        return response.choices[0].message.content.strip()
    
    def gerar_mensagem_relapse(self, dias: int, perdeu: bool, humor) -> str:

        contexto = f"O usuário teve uma recaída após {dias} dias de consistência, no momento ele estava se sentindo {humor}."


        response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": """Você ajuda pessoas a manter disciplina em um app de autocontrole chamado Moderare.

Regras:
- Máximo 2 frases
- Português BR
- Nada genérico
- Nada motivacional clichê
- Nada técnico ou clínico

Tom:
- Direto
- Humano
- Levemente firme
- Sem julgamento pesado

Objetivo:
Responder alguém que acabou de falhar, sem passar pano, mas sem desmotivar.
"""
            },
            {
                "role": "user",
                "content": contexto
            }
        ],
        temperature=0.7,
        max_tokens=60
    )


        return response.choices[0].message.content.strip()
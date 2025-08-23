from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.utils.auth import get_current_user
from app.models import UserResponse
from sqlmodel import Session
from app.database import engine, get_session

router = APIRouter()

# Armazenamento temporário em memória
temp_conversations = {}

questions = [
    "Como você tem se sentido emocionalmente nas últimas semanas?",
    "Quais são os principais desafios que você enfrenta no seu dia a dia?",
    "Você tem conseguido reservar momentos para cuidar de si mesmo? Se sim, quais?",
    "Como você lida com situações de estresse ou ansiedade?",
    "Você sente que tem apoio suficiente das pessoas ao seu redor?",
    "Você já foi diagnosticado com algum transtorno mental? Se quiser, pode compartilhar.",
    "De que forma gostaria que sua rotina diária ajudasse no seu bem-estar?",
    "Há algo mais que você gostaria de acrescentar antes de criarmos seu cronograma personalizado?"
]

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, session: Session = Depends(get_session)):
    session_id = request.session_id
    step = request.step
    message = request.message.strip()

    if session_id not in temp_conversations:
        temp_conversations[session_id] = []

    temp_conversations[session].append({
        "step": step,
        "response": message
    })

    if step < len(questions) - 1:
        next_question = questions[step + 1]
        return ChatResponse(response=next_question, login_required=False)
    else:
        return ChatResponse(
            response="Obrigado por compartilhar. Para salvar suas respostas e gerar seu cronograma, por favor faça login ou cadastro.",
            login_required=True
        )

@router.post("/chat/save-responses")
def save_responses(
    session_id: str,
    current_user = Depends(get_current_user)
):
    if session_id not in temp_conversations:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    responses = temp_conversations[session_id]

    with Session(engine) as session:
        for item in responses:
            db_response = UserResponse(
                user_id=current_user.id,
                step=item["step"],
                response=item["response"]
            )
            session.add(db_response)
        session.commit()

    del temp_conversations[session_id]

    return {"message": "Respostas salvas com sucesso!"}

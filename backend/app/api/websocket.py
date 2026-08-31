from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/lesson/{lesson_id}")
async def lesson_socket(websocket: WebSocket, lesson_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(
                f"Teacher: Continuing lesson {lesson_id}. Student response received: {data}"
            )
    except WebSocketDisconnect:
        pass

import asyncio
import queue
import threading

import socketio
from fastapi import FastAPI,Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

sio = socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi' )
app = FastAPI()
templates = Jinja2Templates(directory="templates")
class CollaborativeEditor:
    def __init__(self):
        self.code = ""
        self.users = {}
        self.sio = None
        self.queue = queue.Queue()
        self.loop = None

    def set_sio(self, sio_instance):
        self.sio = sio_instance

    def update_users(self,sid,username=None):
        self.users[sid] = {}
        self.users[sid]['name']=username
        print(self.users)

    def remove_users(self,sid):
        del self.users[sid]

    def get_users(self):
        return list(self.users.values())

    def get_username(self,sid):
        return self.users.get(sid,None).get('name',None)

    async def edit_code(self, user_id, new_code):
        self.code = new_code
        # Add new code change to queue
        self.queue.put((user_id, self.get_code()))

    #     Here we can add code to push to a redis queue, and a new thread can be started to consume this redis queue.

    def get_code(self):
        return self.code

    async def _emit_text_update(self, user_id, code):  # Async emit function
        await self.sio.emit('text_update', {'text': code, 'user': user_id})

    def process_queue(self):
        while True:
            try:
                user_id, code = self.queue.get(timeout=1.0) #get from queue, wait for 1 sec
                if self.sio:
                    asyncio.run_coroutine_threadsafe(self._emit_text_update(user_id, code), self.loop)
                self.queue.task_done() #signal that the task is complete
            except queue.Empty:
                pass #do nothing if queue is empty
            except Exception as e:
                print(f"Error in queue processing thread: {e}")
                break #or handle the error as needed

    def set_loop(self, param):
        self.loop = param





editor = CollaborativeEditor()
editor.set_sio(sio)


# Connect Sio Client
@sio.event
async def connect(sid,environ):
    print('connect ', sid)
    editor.update_users(sid,None)
    await sio.emit('connected', {'message': 'connected!'}, room=sid)

    # Send initial text to the newly connected client
    await sio.emit('text_update', {'text': editor.get_code(), 'user': "Server"},
                     room=sid)
    await sio.emit('user_list_update', {'users': editor.get_users()})

#Listens for username calls
@sio.on('set_username')
async def handle_set_username(sid, data):
    username = data.get('username')
    if username:
        print(username)
        editor.update_users(sid=sid, username=username)
        print(f"User {sid} set username to {username}")
        await sio.emit('username_set', {'username': username}, room=sid)
        print("here ",editor.get_users())
        await sio.emit('user_list_update', {'users': editor.get_users()})
        print("h2")
    else:
        await sio.emit('username_error', {'message': 'Username cannot be empty.'}, room=sid)

# Listens for code update
@sio.on('text_change')  # New event for text changes
async def handle_text_change(sid, data):
    text = data.get('text')
    if text is not None:
        username = editor.get_username(sid) or "Anonymous"
        await editor.edit_code(username, text)
    else:
        await sio.emit('text_error', {'message': 'Text cannot be empty.'}, room=sid)

# Listens for disconnection to remove user
@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    editor.remove_users(sid)

app.mount("/socket.io", socketio.ASGIApp(sio, app))
app.mount("/static",StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup_event():
    editor.set_loop(asyncio.get_running_loop())  # Get and store the loop
    editor.set_sio(sio) # Set sio instance
    thread = threading.Thread(target=editor.process_queue, daemon=True)
    thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

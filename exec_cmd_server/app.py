import config
import uvicorn
import subprocess
from pydantic import BaseModel
from fastapi import Request, FastAPI
from fastapi.encoders import jsonable_encoder
from rpams import Process, StorageORM

app = FastAPI()

# define db (orm)
storage = StorageORM()
Process.set_session(storage.session)


class CMD(BaseModel):
    command: str


@app.post("/exec")
async def exec(request: Request, cmd: CMD):
    scrubber = ''
    try:
        json_compatible_item_data = jsonable_encoder(cmd)
        scrubber = request.headers.get('scrubber-name')
    except Exception as err:
        print(err)


    try:
        p = subprocess.Popen(json_compatible_item_data['command'].split(" "))
        if 'main.py' in json_compatible_item_data['command']:
            process = Process.get('scrubber', scrubber)

            if process:
                Process.delete(scrubber)
                
            Process.add(p.pid, scrubber)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)

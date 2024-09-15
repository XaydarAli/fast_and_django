import sys
from fastapi_app.app.main import  app
from uvicorn import run
from fastapi_app.app import init_db
def start():
    run("fastapi_app.app.main:app",host="127.0.0.2",port=8002,reload=True)

def main():
    if len(sys.argv) < 2:
        print("manage.py dan keyin kommanda nomini kiriting ")
        sys.exit()

    command = sys.argv[1]
    if command=="run":
        start()

    elif command=="migrate":
        init_db.migrate()

    else:
        print(f"{command}-Unknown command")
        sys.exit()

if __name__=="__main__":
    main()
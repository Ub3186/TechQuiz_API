from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes import user, admin, stats
from routes.question import python, java, c, cpp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#redirecting / route to /docs
@app.get("/")
async def index():
    return RedirectResponse("/docs")

#user route
app.include_router(user.app, tags=["User"])

#admin route
app.include_router(admin.app, tags=["Admin"])

#stats route
app.include_router(stats.app, tags=["Stats"])

#route to handle python question
app.include_router(python.app, tags=["Python"])

#route tot handle java question
app.include_router(java.app, tags=["Java"])

#route tot handle c question
app.include_router(c.app, tags=["C"])

#route tot handle cpp question
app.include_router(cpp.app, tags=["CPP"])

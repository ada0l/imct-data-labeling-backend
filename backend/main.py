from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.core.settings import settings
from backend.handlers import shutdown_handler, startup_handler
from backend.user.api.v1 import router as user_router_v1
from backend.user.api.v1 import me_router as me_user_router_v1
from backend.project.api.v1 import router as project_router_v1
from backend.project_label_type.api.v1 import router as\
    project_label_type_router_v1
from backend.project_label.api.v1 import router as\
    project_label_router_v1
from backend.dataset.api.v1 import router as\
    dataset_router_v1
from backend.image.api.v1 import router as\
    image_router_v1
from backend.label.api.v1 import router as\
    label_router_v1

def get_application():
    _app = FastAPI(**settings.fastapi_kwargs)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.backend_cors_origins
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(user_router_v1, prefix="/user", tags=["user"])
    router_v1.include_router(me_user_router_v1, prefix="/me", tags=["me"])
    router_v1.include_router(project_router_v1,
                             prefix="/project", tags=["project"])
    router_v1.include_router(project_label_type_router_v1,
                             prefix="/projec-label-type",
                             tags=["project-label-type"])
    router_v1.include_router(project_label_router_v1,
                             prefix="/projec-label",
                             tags=["project-label"])
    router_v1.include_router(dataset_router_v1,
                             prefix="/dataset",
                             tags=["dataset"])
    router_v1.include_router(image_router_v1,
                             prefix="/image",
                             tags=["image"])
    router_v1.include_router(label_router_v1,
                             prefix="/label",
                             tags=["label"])
    _app.include_router(router_v1)

    _app.add_event_handler("startup", startup_handler)
    _app.add_event_handler("shutdown", shutdown_handler)

    return _app


app = get_application()

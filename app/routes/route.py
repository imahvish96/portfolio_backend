from fastapi import APIRouter, status;
from app.controllers.information_controller import get_information, add_information, update_information, remove_information
from app.controllers.project_controller import add_project, change_project, get_project
from app.controllers.experience_controller import get_experience, add_experience, change_experience

route = APIRouter(prefix="/api/v1", tags=["Portfolio"])

############# Information Route #########################
route.get('/information', status_code=status.HTTP_200_OK)(get_information)
route.post('/information', status_code=status.HTTP_201_CREATED)(add_information)
route.patch('/information', status_code=status.HTTP_200_OK)(update_information)

############# Project Route #########################
route.get("/project", status_code=status.HTTP_200_OK)(get_project)
route.post("/project", status_code=status.HTTP_201_CREATED)(add_project)
route.patch("/project", status_code=status.HTTP_200_OK)(change_project)
route.delete("/project", status_code=status.HTTP_200_OK)(remove_information)

############# Experience Route #########################
route.get("/experience", status_code=status.HTTP_200_OK)(get_experience)
route.post("/experience", status_code=status.HTTP_201_CREATED)(add_experience)
route.patch("/experience", status_code=status.HTTP_200_OK)(change_experience)
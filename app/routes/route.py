from fastapi import APIRouter, status;
from app.controllers.information_controller import get_information, add_information, update_information, remove_information
from app.controllers.project_controller import add_project, update_project, get_project, delete_project
from app.controllers.experience_controller import get_experience, add_experience, update_experience, delete_experience

route = APIRouter(prefix="/api/v1", tags=["Portfolio"])

############# Information Route #########################
route.get('/information', status_code=status.HTTP_200_OK)(get_information)
route.post('/information', status_code=status.HTTP_201_CREATED)(add_information)
route.patch('/information/{id}', status_code=status.HTTP_200_OK)(update_information)
route.delete('/information/{id}', status_code=status.HTTP_200_OK)(remove_information)

############# Project Route #########################
route.get("/project", status_code=status.HTTP_200_OK)(get_project)
route.post("/project", status_code=status.HTTP_201_CREATED)(add_project)
route.patch("/project/{id}", status_code=status.HTTP_200_OK)(update_project)
route.delete("/project/{id}", status_code=status.HTTP_200_OK)(delete_project)

############# Experience Route #########################
route.get("/experience", status_code=status.HTTP_200_OK)(get_experience)
route.post("/experience", status_code=status.HTTP_201_CREATED)(add_experience)
route.patch("/experience/{id}", status_code=status.HTTP_200_OK)(update_experience)
route.delete("/experience/{id}", status_code=status.HTTP_200_OK)(delete_experience)
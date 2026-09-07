from fastapi import FastAPI

import models.roles_model
import models.users_model
import models.departments_model
import models.designations_model
import models.employees_model
import models.permissions_model
import models.role_permissions_model
import models.salaries_model
import models.projects_model
import models.employee_projects_model
import models.leaves_model
import models.attendance_model

from routes.roles_route import router as roles_router
from routes.users_route import router as users_router
from routes.departments_route import router as departments_router
from routes.designations_route import router as designations_router
from routes.employees_route import router as employees_router
from routes.permissions_route import router as permissions_router
from routes.role_permissions_route import router as role_permissions_router
from routes.salaries_route import router as salaries_router
from routes.projects_route import router as projects_router
from routes.employee_projects_route import router as employee_projects_router
from routes.leaves_route import router as leaves_router
from routes.attendance_route import router as attendance_router
from routes.auth_route import router as auth_router

app = FastAPI()

app.include_router(roles_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(designations_router)
app.include_router(employees_router)
app.include_router(permissions_router)
app.include_router(role_permissions_router)
app.include_router(salaries_router)
app.include_router(projects_router)
app.include_router(employee_projects_router)
app.include_router(leaves_router)
app.include_router(attendance_router)
app.include_router(auth_router)
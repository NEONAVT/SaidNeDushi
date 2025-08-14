from dataclasses import dataclass

from poetry.repositories.cached_repository import CachedRepository

from exceptions import TaskNotFound, CategoryExistAlready, CategoryNotFound
from repository import TaskCache
from repository.tasks import TaskRepository, CategoryRepository
from schemas import TaskSchema
from schemas.tasks import TaskCreateSchema, CategoryCreateSchema, CategorySchema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


@dataclass
class TasksService:
    tasks_repository: TaskRepository
    tasks_cache: TaskCache

    def create_task(self,
            task: TaskCreateSchema,
            user_id: int
    ) -> TaskSchema:
        task_id = self.tasks_repository.create_task(task, user_id)
        task = self.tasks_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    def get_task_by_id(self,
            task_id: int,
    ) -> TaskSchema:
        task = self.tasks_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    def get_all_tasks(self) -> list[TaskSchema]:
        if tasks := self.tasks_cache.get_tasks():
            return tasks
        else:
            tasks = self.tasks_repository.get_all_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.tasks_cache.set_tasks(tasks_schema)
            return tasks_schema

    def update_task_name(self, task_id: int, body: str, user_id: int) -> TaskSchema:
        task = self.tasks_repository.update_task_name(task_id=task_id, user_id=user_id, name=body)
        if not task:
            raise TaskNotFound
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: int, user_id: int):
        self.tasks_repository.delete_task(task_id=task_id, user_id=user_id)

@dataclass
class CategoryService:

    category_repository: CategoryRepository

    def create_category(self,
                        category: CategoryCreateSchema
                        ) -> CategorySchema:
        try:
            category_id = self.category_repository.create_category(category)
            category = self.category_repository.get_category(category_id)
            return CategorySchema.model_validate(category)
        except IntegrityError:
            raise CategoryExistAlready

    def get_all_categories(self) -> list[CategorySchema]:
        categories = self.category_repository.get_all_categories()
        categories_schema = [CategorySchema.model_validate(category) for category in categories]
        return categories_schema

    def get_category_by_id(self, category_id: int) -> CategorySchema:
        category = self.category_repository.get_category(category_id)
        if not category:
            raise CategoryNotFound
        return CategorySchema.model_validate(category)

    def update_category(self, category_id: int, name: str, type: str) -> CategorySchema:
        category = self.category_repository.update_category(category_id=category_id, name=name, type=type)
        if not category:
            raise CategoryNotFound
        return CategorySchema.model_validate(category)

    def delete_category(self, category_id: int):
        self.category_repository.delete_category(category_id=category_id)

from typing import Sequence

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from models import Tasks, Categories
from schemas.tasks import TaskCreateSchema, CategoryCreateSchema


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = (
            insert(Tasks)
            .values(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id,
                    user_id=user_id)
            .returning(Tasks.id)
        )
        with self.db_session as session:
            task_id = session.execute(query).scalar_one_or_none()
            session.commit()
            return task_id

    def get_all_tasks(self) -> Sequence[Tasks]:
        with self.db_session as session:
            tasks: Sequence[Tasks] = session.execute(select(Tasks)).scalars().all()
        return tasks


    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session as session:
            task: Tasks = (
                session.execute(
                    select(Tasks).where(Tasks.id == task_id))
            ).scalar_one_or_none()
        return task

    def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = (
            select(Tasks, Categories)
            .join(Categories, Categories.id == Tasks.category_id)
            .where(Tasks.id == task_id, Tasks.user_id == user_id)
        )
        with self.db_session as session:
            task: Tasks = session.execute(query).scalar_one_or_none()
        return task

    def update_task_name(self, task_id: int, user_id: int, name: str) -> Tasks | None:
        query = (
            update(Tasks)
            .where(Tasks.id == task_id, Tasks.user_id == user_id)
            .values(name=name)
            .returning(Tasks)
        )
        with self.db_session as session:
            updated_task = session.execute(query).scalar_one_or_none()
            session.commit()
            return updated_task

    def delete_task(self, task_id: int, user_id: int):
        query = (
            delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        )
        with self.db_session as session:
            session.execute(query)
            session.commit()


class CategoryRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_category(self, category: CategoryCreateSchema) -> int:
        query = (
            insert(Categories)
            .values(name=category.name, type=category.type)
            .returning(Categories.id)
        )
        with self.db_session as session:
            category_id = session.execute(query).scalar_one_or_none()
            session.commit()
            return category_id


    def get_category(self, category_id: int) -> Categories:
        with self.db_session as session:
            category: Categories = (
                session.execute(
                    select(Categories).where(Categories.id==category_id))
                ).scalar_one_or_none()
        return category


    def get_all_categories(self) -> Sequence[Categories]:
        with self.db_session as session:
            categories: Sequence[Categories] = session.execute(select(Categories)).scalars().all()
        return categories

    def update_category(self, category_id: int, name: str, type: str) -> Categories | None:
        query = (
            update(Categories)
            .where(Categories.id == category_id)
            .values(name=name, type=type)
            .returning(Categories)
        )
        with self.db_session as session:
            updated_category = session.execute(query).scalar_one_or_none()
            session.commit()
            return updated_category

    def delete_category(self, category_id: int):
        query = (
            delete(Categories).where(Categories.id == category_id)
        )
        with self.db_session as session:
            session.execute(query)
            session.commit()


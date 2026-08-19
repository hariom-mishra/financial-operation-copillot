from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from models.expenses import GetExpenses, SearchExpenses, AddExpenses, UpdateExpenses
from schema.expenses import Expenses
from core.exceptions import ExpenseException
from typing import Optional
from datetime import date, datetime, timezone

class ExpenseRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_expenses(self, user_id: int, limit: int, offset: int, category: Optional[str], from_date: Optional[datetime], to_date: Optional[datetime]):
        try:
            query = select(Expenses).where(Expenses.user_id == user_id)
            if category:
                query = query.where(Expenses.category == category)
            if from_date:
                query = query.where(Expenses.date >= from_date)
            if to_date:
                query = query.where(Expenses.date <= to_date)
            query = query.order_by(Expenses.date.desc()).limit(limit).offset(offset)
            res = await self.db.execute(query)
            return res.scalars().all()
        except Exception as e:
            raise ExpenseException(str(e))

    async def add_expense(self, expense_data: AddExpenses, user_id: int):
        try:
            expense_date = expense_data.date if expense_data.date else datetime.now(timezone.utc)
            new_expense = Expenses(
                amount=expense_data.amount,
                category=expense_data.category,
                description=expense_data.description,
                date=expense_date,
                user_id=user_id
            )
            self.db.add(new_expense)
            await self.db.commit()
            await self.db.refresh(new_expense)
            return new_expense
        except Exception as e:
            await self.db.rollback()
            raise ExpenseException(message=str(e))

    async def search_expenses(self, user_id: int, keyword: str, limit: int = 20, offset: int = 0):
        try:
            pattern = f"%{keyword}%"
            query = (
                select(Expenses)
                .where(Expenses.user_id == user_id)
                .where(
                    or_(
                        Expenses.category.ilike(pattern),
                        Expenses.description.ilike(pattern),
                    )
                )
                .order_by(Expenses.date.desc())
                .limit(limit)
                .offset(offset)
            )
            res = await self.db.execute(query)
            return res.scalars().all()
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_summary(self, user_id: int, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None):
        try:
            base_filter = [Expenses.user_id == user_id]
            if from_date:
                base_filter.append(Expenses.date >= from_date)
            if to_date:
                base_filter.append(Expenses.date <= to_date)

            # Per-category aggregation
            cat_query = (
                select(
                    Expenses.category,
                    func.sum(Expenses.amount).label("total"),
                    func.count(Expenses.id).label("count"),
                )
                .where(*base_filter)
                .group_by(Expenses.category)
                .order_by(func.sum(Expenses.amount).desc())
            )
            cat_res = await self.db.execute(cat_query)
            by_category = cat_res.fetchall()

            total_spent = sum(row.total for row in by_category)
            expense_count = sum(row.count for row in by_category)

            return {
                "total_spent": total_spent,
                "expense_count": expense_count,
                "by_category": [
                    {"category": row.category, "total": row.total, "count": row.count}
                    for row in by_category
                ],
            }
        except Exception as e:
            raise ExpenseException(str(e))

    async def update_expense(self, expense_id: int, user_id: int, data: UpdateExpenses):
        try:
            query = select(Expenses).where(Expenses.id == expense_id, Expenses.user_id == user_id)
            res = await self.db.execute(query)
            expense = res.scalar_one_or_none()
            if not expense:
                raise ExpenseException(f"Expense {expense_id} not found", status_code=404)

            # Only update fields that were explicitly provided
            update_data = data.model_dump(exclude_none=True)
            for field, value in update_data.items():
                setattr(expense, field, value)

            await self.db.commit()
            await self.db.refresh(expense)
            return expense
        except ExpenseException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise ExpenseException(str(e))

    async def delete_expense(self, expense_id: int, user_id: int):
        try:
            query = select(Expenses).where(Expenses.id == expense_id, Expenses.user_id == user_id)
            res = await self.db.execute(query)
            expense = res.scalar_one_or_none()
            if not expense:
                raise ExpenseException(f"Expense {expense_id} not found", status_code=404)

            await self.db.delete(expense)
            await self.db.commit()
            return {"message": f"Expense {expense_id} deleted successfully"}
        except ExpenseException:
            raise
        except Exception as e:
            await self.db.rollback()
            raise ExpenseException(str(e))

        
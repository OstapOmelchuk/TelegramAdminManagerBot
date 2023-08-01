from sqlalchemy import Column, BigInteger, String, sql, DateTime, Boolean, ForeignKey, UniqueConstraint

from db.db_connection import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "User"
    user_id = Column(BigInteger, nullable=False, primary_key=True)
    fullname = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    mail = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    status = Column(String(25), default="active")
    subscription_status = Column(Boolean, nullable=False, default=False)
    subscription_start_date = Column(DateTime, default=None)
    subscription_end_date = Column(DateTime, default=None)
    is_admin = Column(Boolean, nullable=False, default=False)

    query: sql.select


class Payment(TimedBaseModel):
    __tablename__ = "Payment"
    payment_id = Column(BigInteger, nullable=False, primary_key=True)
    tx_id = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey(User.user_id), nullable=False)

    __table_args__ = (
        UniqueConstraint('tx_id', name='uq_tx_id'),
    )

    query: sql.select

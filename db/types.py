from enum import Enum


class TransactionStatus(str, Enum):
    created = "created"
    confirmed = "confirmed"
    cancelled = "cancelled"
    error = "error"


class TransactionSymbol(str, Enum):
    plus = "+"
    minus = "-"


class ActionsCashUsersCB(str, Enum):
    top_up = "Top up"
    transfer = "Transfer"
    withdraw = "Withdraw"
    extract = "Extract"
    extract_user = "Extract user"


class ActionsCashUsersTransferCB(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"


class OrderStatus(str, Enum):
    awaiting_payment = "awaiting-payment"  # Ожидание оплаты
    payment_offline = "payment-offline"  # Оплата при получении
    payment_received = "payment-received"  # Оплачено
    partially_paid = "partially-paid"  # Частичная оплата
    completed = "active"  # Выполнен
    dispatched = "dispatched"  # Отменено


class NotificationTypes(str, Enum):
    confirm_order = "confirm_order"  # Order confirm success
    pay_order = "pay_order"  # Success payment order
    new_user = "new_user"  # Register new user

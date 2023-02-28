from connectors import ConnectorRouter
from sqlalchemy import text

from alertlib.bot.bot import TelegramBot
from postgres.engine import engine as postgres_engine
from settings import TG_BOT_TOKEN, TG_ERRORS_CHAT_ID, TG_CHAT_ID


def get_binance_bnb_balance(api_key: str,
                            secret_key: str,
                            section: str) -> float:
    token_symbol = "BNB"

    cex_con = ConnectorRouter(
        exchange="Binance",
        section=section
    ).init_connector(
        api_key,
        secret_key
    )

    cex_balances = cex_con.get_balances()

    cex_token_bal = cex_balances[token_symbol]['total'] if token_symbol in cex_balances else 0

    return cex_token_bal


def send_binance_bnb_balance_alert(label: str,
                                   section: str,
                                   current_balance: float or int) -> None:
    bot = TelegramBot(token=TG_BOT_TOKEN)

    text = (
        "@alexs7a @ia_andriyanov @old_evgeny\n"
        "<b>BNB BALANCE ALERT</b>\n"
        f"{label}: {section}\n"
        f"current balance: {current_balance:.3f} BNB"
    )

    bot.send_message(
        text=text,
        chat=TG_CHAT_ID
    )


def send_error_alert(error_text: str) -> None:
    bot = TelegramBot(token=TG_BOT_TOKEN)

    text = (
        "<b>BNB BALANCE ALERTS MODULE</b>\n"
        f"{error_text}"
    )

    bot.send_message(
        text=text,
        chat=TG_ERRORS_CHAT_ID
    )


def get_previous_alerts_count(alert_type: str, timedelta_in_minutes: int) -> int:
    stmt = text(f"""
    select count(*)
    from alerts
    where
        type = '{alert_type}' and
        creation_datetime between timezone('utc', now()) - interval '{timedelta_in_minutes} minutes' 
        and timezone('utc', now()) 
    """)

    with postgres_engine.connect() as conn:
        res = conn.execute(stmt).all()
        return res[0][0] if res and res[0] else 0


def commit_alert_into_db(alert_type: str):
    stmt = text(f"""
        INSERT INTO alerts (type, creation_datetime)
        VALUES ('{alert_type}', timezone('utc', now()))
    """)

    with postgres_engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

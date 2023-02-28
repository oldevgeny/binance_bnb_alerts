import traceback

from operations import get_binance_bnb_balance, send_binance_bnb_balance_alert, get_previous_alerts_count, \
    commit_alert_into_db, send_error_alert
from settings import CONFIGS, ALERT_TIME_THRESHOLD_IN_MINUTES


def main():
    for config in CONFIGS:
        binance_bnb_balance = get_binance_bnb_balance(api_key=config["api_key"],
                                                  secret_key=config["secret_key"],
                                                  section=config["section"])
        if binance_bnb_balance > config["threshold"]:
            continue

        label = config["label"]
        section = config["section"]

        alert_type = f"binance_bnb_alerts:{label}_{section}"

        previous_alerts_count = get_previous_alerts_count(
            alert_type=alert_type,
            timedelta_in_minutes=ALERT_TIME_THRESHOLD_IN_MINUTES
        )

        if previous_alerts_count > 0:
            continue

        send_binance_bnb_balance_alert(label=config["label"],
                                       section=config["section"],
                                       current_balance=binance_bnb_balance)
        commit_alert_into_db(alert_type=alert_type)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_text = f"ERROR main(): {e}\n\n" + f"traceback: {traceback.format_exc()}"
        print(error_text)

        send_error_alert(error_text=str(e))

import time
from datetime import datetime
from tools.stock_monitor_tool import StockMonitorTool
from plyer import notification

CHECK_INTERVAL = 60  # seconds

def run_scheduler():
    monitor = StockMonitorTool()

    print("═══════════════════════════════════════════")
    print("   Stock Monitoring Scheduler Started")
    print(f"   Checking alerts every {CHECK_INTERVAL} seconds")
    print("═══════════════════════════════════════════")

    while True:
        try:
            print(f"[{datetime.now()}] Checking alerts...")

            result = monitor.check_alerts()

            if result["status"] == "success" and result["data"]:
                print("ALERTS TRIGGERED")
                for alert in result["data"]:
                    print("----------------------------------------")
                    print(f" Symbol:     {alert['symbol']}")
                    print(f" Price:      {alert['price']}")
                    print(f" Threshold:  {alert['threshold']}")
                    print(f" Message:    {alert['message']}")
                    print("----------------------------------------")

                    # TODO:
                    # Replace print with:
                    # send_email(...)
                    # send_sms(...)
                    # send_telegram(...)
                    # post_to_discord(...)

                print("═══════════════════════════════════════════")
                #with open("notifications.log", "a") as f:
                 #   f.write(alert["message"] + "\n")
                notification.notify(
                title="Stock Alert",
                message=alert["message"],
                timeout=5
                )
                with open("notifications.log", "a") as f:
                    f.write(alert["message"] + "\n")


            elif result["status"] == "error":
                print("Error checking alerts:", result["error_message"])

        except Exception as e:
            print(f"Unexpected scheduler error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_scheduler()

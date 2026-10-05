import json
import os
import shutil
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = PROJECT_DIR / "email_config.json"


def get_email_settings():
    # 1. Try loading from email_config.json first
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            settings = {
                "REPORT_EMAIL_USERNAME": config.get("REPORT_EMAIL_USERNAME"),
                "REPORT_EMAIL_APP_PASSWORD": config.get("REPORT_EMAIL_APP_PASSWORD"),
                "REPORT_EMAIL_TO": config.get("REPORT_EMAIL_TO"),
            }
    else:
        # 2. Fall back to environment variables
        settings = {
            "REPORT_EMAIL_USERNAME": os.environ.get("REPORT_EMAIL_USERNAME"),
            "REPORT_EMAIL_APP_PASSWORD": os.environ.get("REPORT_EMAIL_APP_PASSWORD"),
            "REPORT_EMAIL_TO": os.environ.get("REPORT_EMAIL_TO"),
        }

    missing_settings = [name for name, value in settings.items() if not value]
    if missing_settings:
        raise RuntimeError(
            f"Missing email configuration: {', '.join(missing_settings)}. "
            f"Please update {CONFIG_FILE.name} or set environment variables."
        )

    return settings


def main():
    print(f"Starting pytest in {PROJECT_DIR}", flush=True)
    test_result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--alluredir=allure-results"],
        check=False,
        cwd=PROJECT_DIR,
    )

    print("Generating Allure Report...", flush=True)
    subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        check=True,
        cwd=PROJECT_DIR,
        shell=True,
    )

    # Archive the allure-report directory to zip
    report_dir = PROJECT_DIR / "allure-report"
    zip_path = PROJECT_DIR / "allure-report"

    if report_dir.exists():
        print("Archiving Allure report to ZIP...", flush=True)
        shutil.make_archive(
            base_name=str(zip_path), format="zip", root_dir=str(report_dir)
        )
    else:
        raise FileNotFoundError(f"Report directory not found at {report_dir}")

    zip_file_path = PROJECT_DIR / "allure-report.zip"

    # Load email settings from JSON
    email_settings = get_email_settings()
    email_username = email_settings["REPORT_EMAIL_USERNAME"]
    email_password = email_settings["REPORT_EMAIL_APP_PASSWORD"]
    email_to = email_settings["REPORT_EMAIL_TO"]

    msg = EmailMessage()
    msg["Subject"] = "ParaBank Automation Test Run Finished"
    msg["From"] = email_username
    msg["To"] = email_to
    test_status = "passed" if test_result.returncode == 0 else "failed"

    msg.set_content(
        "Hi Team,\n\n"
        f"The ParaBank automation test run has finished with status: {test_status}.\n"
        f"Pytest exit code: {test_result.returncode}.\n\n"
        "Please find the attached 'allure-report.zip' containing the HTML test report."
    )

    # Attach the generated zip file
    if zip_file_path.exists():
        with open(zip_file_path, "rb") as f:
            file_data = f.read()
            file_name = zip_file_path.name

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="zip",
            filename=file_name,
        )

    print("Sending email notification with report attachment...", flush=True)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.send_message(msg)

    print("Report notification emailed successfully.")

    # Clean up local zip file after sending
    if zip_file_path.exists():
        zip_file_path.unlink()

    return test_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
clickjack-scanner/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── header_scanner.py        # later: CSP + XFO detection
│   │   ├── selenium_scanner.py      # later: PoC testing + screenshots
│   │   ├── report_generator.py      # PDF/HTML report creation
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── scan.py                  # later: main endpoint /scan
│   │
│   ├── utils/
│   │   ├── file_ops.py              # file save/delete helpers
│   │   ├── selenium_driver.py       # driver builder
│   │
│   ├── static/
│   │   └── reports/                 # generated reports saved here
│   │
│   ├── templates/
│   │   └── report_template.html     # to render reports
│   │
│   ├── main.py
│   ├── __init__.py
│
├── tests/
│   └── test_sample.py
│
├── selenium/
│   ├── Dockerfile.chromium          # optional: chromium + selenium
│   ├── requirements.txt
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Dockerfile




###
✔ Create /scan API
✔ Integrate header scanner
✔ Integrate Selenium PoC attacker page generator
✔ Auto screenshots + evidence capture
✔ Generate downloadable report (PDF/HTML)
✔ Add Docker support for FastAPI + Chromium
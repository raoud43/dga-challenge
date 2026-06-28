# استخدام نسخة خفيفة من بايثون
FROM python:3.12-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات (تأكد من وجود requirements.txt في مجلد backend)
COPY requirements.txt .

# تثبيت المكتبات (بما في ذلك fastapi, uvicorn, pydantic-settings)
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كامل كود الباك اند إلى الحاوية
COPY . .

# المنفذ الذي سيعمل عليه FastAPI
EXPOSE 8000

# الأمر الذي سيشغل السيرفر
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=koreanparts.settings

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (optional)
# RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the application port
EXPOSE 8000


# Collect css files (run at build time if necessary)


# Start app: run migrations, collectstatic, then launch gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 koreanparts.wsgi:application"]
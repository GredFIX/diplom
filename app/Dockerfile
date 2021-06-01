FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV ADMIN_PWD "9f7587b8ea6ce66a35aa89ec89b0950076c1e0d23e5e7830dca4031555a97354:ca4243cf8c1a4f20b76eade24297eb28"
EXPOSE 5000

CMD [ "python", "app.py" ]

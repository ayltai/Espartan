FROM node:24-trixie-slim AS build
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app/frontend
COPY frontend/ .
RUN pnpm i --force
RUN pnpm build

FROM python:3.13-slim-trixie
WORKDIR /app
COPY backend/ ./
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt
COPY --from=build /app/frontend/dist ./web
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0"]

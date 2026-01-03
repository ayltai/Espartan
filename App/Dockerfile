FROM node:24-trixie-slim AS build
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app
COPY . .
RUN pnpm i --force
EXPOSE 8081
CMD ["pnpm", "start"]

FROM golang:1.24-alpine

WORKDIR /app_vanila

COPY go.mod go.sum ./
RUN go mod tidy

COPY . .
RUN go build -o research /app

EXPOSE 3000

CMD ["./research"]

FROM golang:1.24-alpine

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod tidy

COPY . .
RUN go build -o myapp .

EXPOSE 3000

CMD ["./myapp"]

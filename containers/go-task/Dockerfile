# syntax=docker/dockerfile:1

FROM golang:1.24-alpine AS build

# Set destination for COPY
WORKDIR /app

# Download any Go modules
COPY ./containers/go-task/go.mod ./
RUN go mod download

# Copy container source code
COPY ./containers/go-task/*.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-task

FROM scratch
COPY --from=build /go-task /go-task
EXPOSE 8080

# Run
CMD ["/go-task"]

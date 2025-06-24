import { Container } from "@cloudflare/containers";

export class PythonFastAPIContainer extends Container<Env> {
  defaultPort = 8081;
  sleepAfter = "1m";

  envVars = {
    MESSAGE: "I was passed in via the container class!",
  };
}

export class GoTaskContainer extends Container<Env> {
  defaultPort = 8080;
  sleepAfter = "1m";

  envVars = {
    MESSAGE: "I was passed in via the container class!",
  };
}

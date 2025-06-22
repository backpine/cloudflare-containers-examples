import { Container } from "@cloudflare/containers";

export class PythonFastAPIContainer extends Container<Env> {
  defaultPort = 8081;
  sleepAfter = "1m";

  envVars = {
    MESSAGE: "I was passed in via the container class!",
  };

  override onStart() {
    console.log("Container successfully started");
  }

  override onStop() {
    console.log("Container successfully shut down");
  }

  override onError(error: unknown) {
    console.log("Container error:", error);
  }
}

export class GoTaskContainer extends Container<Env> {
  defaultPort = 8080;
  sleepAfter = "1m";

  envVars = {
    MESSAGE: "I was passed in via the container class!",
  };

  override onStart() {
    console.log("Container successfully started");
  }

  override onStop() {
    console.log("Container successfully shut down");
  }

  override onError(error: unknown) {
    console.log("Container error:", error);
  }
}

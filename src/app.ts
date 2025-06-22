import { Hono } from "hono";
import { getContainer, loadBalance } from "@cloudflare/containers";

export const App = new Hono<{ Bindings: Env }>();

App.get("/", (c) => {
  return c.text("Hello Hono!");
});

App.get("/python-container", (c) => {
  const containerService = getContainer(c.env.PYTHON_CONTAINER, "instance-1");
  // notice we place the raw request in the fetch method
  // our container service has the same path /python-container
  // which means the raw request will contain the path /python-container
  return containerService.fetch(c.req.raw);
});

App.get("/python-container/load-balance", async (c) => {
  const containerService = await loadBalance(c.env.PYTHON_CONTAINER, 3);
  // Notice that we are fetching the load-balanced URL
  // we can access specific container paths by useing https://<any-name>/<path>
  return await containerService.fetch("http://python-container/load-balance");
});

App.get("/go-task", async (c) => {
  const containerService = getContainer(
    c.env.GO_TASK_CONTAINER,
    "single-go-task",
  );

  return await containerService.fetch("http://go-task/");
});

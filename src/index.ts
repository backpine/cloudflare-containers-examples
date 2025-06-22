export { PythonFastAPIContainer } from "@/container-services";
export { GoTaskContainer } from "@/container-services";

import { App } from "@/app";

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext,
  ): Promise<Response> {
    return App.fetch(request, env, ctx);
  },
};

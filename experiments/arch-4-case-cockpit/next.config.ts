import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // The worker shells out to agent CLIs and simple-git; both need
  // to run on the server side only. Nothing to configure for the MVP.
  experimental: {
    // Next 15 server actions are enabled by default.
  },
  // The vault cache lives outside the Next build output.
  outputFileTracingIncludes: {
    "/api/**/*": [],
  },
};

export default nextConfig;

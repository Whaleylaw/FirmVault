import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cockpit: {
          bg: "#0b0f14",
          panel: "#121821",
          edge: "#1f2937",
          accent: "#38bdf8",
          ok: "#34d399",
          warn: "#fbbf24",
          err: "#f87171",
        },
      },
      fontFamily: {
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;

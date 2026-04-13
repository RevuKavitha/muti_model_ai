import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#06080d",
        panel: "#0b0f17",
        border: "#1f2a3d",
        accent: "#ef4444",
        success: "#22c55e",
      },
      fontFamily: {
        display: ["Space Grotesk", "ui-sans-serif", "system-ui"],
        body: ["Manrope", "ui-sans-serif", "system-ui"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(239,68,68,0.25), 0 20px 50px rgba(0,0,0,0.45)",
      },
    },
  },
  plugins: [],
};

export default config;

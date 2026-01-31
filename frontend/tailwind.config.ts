import type { Config } from "tailwindcss";

/**
 * Tailwind config for multi-school platform.
 * Dynamic theming (primary_color, secondary_color) applied via CSS variables
 * from school config; see useSchoolConfig and globals.css.
 */
const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary, #0A3D62)",
        secondary: "var(--color-secondary, #EAF2F8)",
      },
    },
  },
  plugins: [],
};

export default config;

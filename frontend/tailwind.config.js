/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#030014", // Deep Midnight
                surface: "#0f0c29",    // Dark Violet-Black
                card: "rgba(30, 27, 75, 0.4)", // Glassy Blue
                primary: "#6366f1",    // Indigo
                secondary: "#a855f7",  // Purple
                accent: "#ec4899",     // Pink
                success: "#10b981",    // Emerald
                "text-glow": "#e0e7ff",
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Plus Jakarta Sans', 'sans-serif'],
            },
            animation: {
                'blob': 'blob 7s infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
            },
            keyframes: {
                blob: {
                    "0%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                    "33%": {
                        transform: "translate(30px, -50px) scale(1.1)",
                    },
                    "66%": {
                        transform: "translate(-20px, 20px) scale(0.9)",
                    },
                    "100%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                },
                glow: {
                    "0%": { boxShadow: "0 0 5px #6366f1" },
                    "100%": { boxShadow: "0 0 20px #a855f7, 0 0 10px #6366f1" }
                }
            },
            backdropBlur: {
                xs: '2px',
            }
        },
    },
    plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	daisyui: {
		themes: [
			{
				gruvbox: {
					"primary": "#3c3836",
					"secondary": "#fbf1c7",
					"accent": "#fabd2f",
					"neutral": "#282828",
					"base-100": "#2b2b2b",
					"info": "#83a598",
					"success": "#98971a",
					"warning": "#d65d0e",
					"error": "#cc241d",
				},
			},
		],
	},
	plugins: [require("daisyui")],
};

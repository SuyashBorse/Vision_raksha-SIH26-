/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      colors: {
        // VisionRaksha Healthcare AI Color Palette
        navy: {
          DEFAULT: '#1F2F42',
          light: '#26394D',
          dark: '#162233',
        },
        teal: {
          DEFAULT: '#22AEB0',
          bright: '#38C4C4',
          soft: '#76D6D2',
          light: '#E8F7F6',
          hover: '#1D9A9C',
        },
        medical: {
          bg: '#F7FAFB',
          white: '#FFFFFF',
        },
        vr: {
          text: '#263746',
          'text-secondary': '#657685',
          'text-muted': '#94A1AB',
          border: '#E1E9EC',
        },

        // Functional color overrides
        primary: {
          DEFAULT: '#22AEB0',
          hover: '#1D9A9C',
          light: '#E8F7F6',
        },
        secondary: {
          DEFAULT: '#26394D',
          hover: '#1F2F42',
        },
        accent: {
          DEFAULT: '#38C4C4',
          hover: '#22AEB0',
        },
        support: {
          DEFAULT: '#76D6D2',
          border: '#E1E9EC',
        },
        muted: {
          DEFAULT: '#94A1AB',
        },
      },
      boxShadow: {
        'card': '0 2px 12px 0 rgba(34, 174, 176, 0.08)',
        'card-hover': '0 8px 30px 0 rgba(34, 174, 176, 0.15)',
        'nav': '0 2px 20px 0 rgba(31, 47, 66, 0.12)',
        'btn': '0 4px 14px 0 rgba(34, 174, 176, 0.35)',
        'btn-hover': '0 6px 20px 0 rgba(34, 174, 176, 0.45)',
        'soft': '0 1px 6px 0 rgba(34, 174, 176, 0.06)',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out forwards',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'float': 'float 6s ease-in-out infinite',
        'pulse-soft': 'pulseSoft 3s ease-in-out infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
};

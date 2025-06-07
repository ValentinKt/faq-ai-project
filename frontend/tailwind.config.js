module.exports = {
    content: [
      './index.html',
      './src/**/*.{js,ts,jsx,tsx}',
    ],
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          primary: {
            DEFAULT: '#3b82f6',
            50: '#eff6ff',
            100: '#dbeafe',
            200: '#bfdbfe',
            300: '#93c5fd',
            400: '#60a5fa',
            500: '#3b82f6',
            600: '#2563eb',
            700: '#1d4ed8',
            800: '#1e40af',
            900: '#1e3a8a',
          },
          secondary: {
            DEFAULT: '#8b5cf6',
            50: '#f5f3ff',
            100: '#ede9fe',
            200: '#ddd6fe',
            300: '#c4b5fd',
            400: '#a78bfa',
            500: '#8b5cf6',
            600: '#7c3aed',
            700: '#6d28d9',
            800: '#5b21b6',
            900: '#4c1d95',
          },
          background: {
            DEFAULT: '#f8fafc',
            dark: '#0f172a',
            card: '#ffffff',
            'card-dark': '#1e293b',
          },
          text: {
            primary: '#1e293b',
            'primary-dark': '#f1f5f9',
            secondary: '#64748b',
            'secondary-dark': '#cbd5e1',
          },
          border: {
            DEFAULT: '#e2e8f0',
            dark: '#334155',
          },
          success: {
            DEFAULT: '#10b981',
            dark: '#047857',
          },
          warning: {
            DEFAULT: '#f59e0b',
            dark: '#b45309',
          },
          danger: {
            DEFAULT: '#ef4444',
            dark: '#b91c1c',
          },
        },
        boxShadow: {
          card: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          'card-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
          button: '0 4px 6px -1px rgba(59, 130, 246, 0.3), 0 2px 4px -1px rgba(59, 130, 246, 0.2)',
        },
        borderRadius: {
          DEFAULT: '0.5rem',
          lg: '0.75rem',
        },
        animation: {
          'fade-in': 'fadeIn 0.3s ease-in-out',
        },
        keyframes: {
          fadeIn: {
            '0%': { opacity: 0 },
            '100%': { opacity: 1 },
          },
        },
      },
    },
    plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
    ],
  };
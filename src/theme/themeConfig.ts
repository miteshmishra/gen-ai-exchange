import { createTheme } from '@mui/material/styles';
import type { ThemeOptions } from '@mui/material/styles';

export const getDesignTokens = (mode: 'light' | 'dark'): ThemeOptions => ({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          // Light mode colors
          primary: {
            main: '#1a73e8',
            light: '#4285f4',
            dark: '#1557b0',
          },
          secondary: {
            main: '#188038',
            light: '#34a853',
            dark: '#0d652d',
          },
          background: {
            default: '#ffffff',
            paper: '#f8f9fa',
          },
          text: {
            primary: '#202124',
            secondary: '#5f6368',
          },
          divider: 'rgba(0, 0, 0, 0.12)',
          action: {
            hover: 'rgba(0, 0, 0, 0.04)',
            selected: 'rgba(0, 0, 0, 0.08)',
          },
        }
      : {
          // Dark mode colors
          primary: {
            main: '#8ab4f8',
            light: '#adc6f5',
            dark: '#669df6',
          },
          secondary: {
            main: '#188038',
            light: '#34a853',
            dark: '#0d652d',
          },
          background: {
            default: '#1e1e1e',
            paper: '#2d2d2d',
          },
          text: {
            primary: '#ffffff',
            secondary: 'rgba(255, 255, 255, 0.7)',
          },
          divider: 'rgba(255, 255, 255, 0.12)',
          action: {
            hover: 'rgba(255, 255, 255, 0.08)',
            selected: 'rgba(255, 255, 255, 0.12)',
          },
        }),
  },
  typography: {
    fontFamily: '"Google Sans", "Roboto", "Arial", sans-serif',
    h1: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.75rem',
      lineHeight: 1.4,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarColor: "#6b6b6b #2b2b2b",
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "#2b2b2b",
            width: '8px',
            height: '8px',
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 4,
            backgroundColor: "#424242",
            minHeight: 24,
            border: "2px solid #2b2b2b",
          },
          "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover": {
            backgroundColor: "#525252",
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          '&.MuiDrawer-paper': {
            borderRight: '1px solid',
            borderColor: 'divider'
          }
        }
      }
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          borderBottom: 'none',
          minHeight: '64px',
          height: '64px',
        },
      },
    },
    MuiToolbar: {
      styleOverrides: {
        root: {
          minHeight: '64px !important',
          height: '64px',
          paddingLeft: '16px',
          paddingRight: '16px',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 4,
          padding: '4px 12px',
          fontSize: '0.875rem',
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontSize: '1rem',
          padding: '8px 12px',
          minHeight: '40px',
          '& .MuiInputBase-input': {
            padding: '4px 0',
            '&::placeholder': {
              opacity: 0.7
            }
          }
        },
      },
    },
  },
  shape: {
    borderRadius: 4,
  },
});
import { AppBar, Toolbar, Typography, Avatar, Box, IconButton, useTheme } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

interface HeaderProps {
  onMenuClick: () => void;
  isMobile: boolean;
  isCollapsed?: boolean;
  onToggleTheme: () => void;
  mode: 'light' | 'dark';
}

const Header = ({ onMenuClick, isMobile, isCollapsed = false, onToggleTheme, mode }: HeaderProps) => {
  const theme = useTheme();
  return (
    <AppBar 
      position="fixed"
      sx={{
        width: { sm: isCollapsed ? 'calc(100% - 72px)' : 'calc(100% - 280px)' },
        ml: { sm: isCollapsed ? '72px' : '280px' },
        transition: theme => theme.transitions.create(['width', 'margin'], {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
        }),
      }}
    >
      <Toolbar 
        disableGutters
        sx={{
          height: '64px',
          minHeight: '64px !important',
          py: '12px',
          backgroundImage: 'none',
          '&.MuiToolbar-root': {
            height: '64px',
            minHeight: '64px !important',
            backgroundImage: 'none',
            borderBottom: 'none'
          }
        }}
      >
        <Box sx={{ 
          ml: 2, 
          display: 'flex', 
          alignItems: 'center',
          overflow: 'hidden',
          transition: theme => theme.transitions.create('opacity', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          ...(isCollapsed && {
            opacity: 0,
            width: 0,
            ml: 0
          })
        }}>
          <Typography
            variant="body1"
            noWrap
            component="div"
            sx={{ 
              color: 'text.primary', 
              fontWeight: 500,
              fontSize: '0.9rem'
            }}
          >
            AI Trip Planner
          </Typography>
        </Box>

        <Box sx={{ 
          ml: 'auto', 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1, 
          mr: 1,
          transition: theme => theme.transitions.create(['opacity', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          ...(isCollapsed && {
            '& .MuiButton-root': {
              opacity: 0,
              width: 0,
              padding: 0,
              margin: 0,
              border: 0
            }
          })
        }}>
          <IconButton
            onClick={onToggleTheme}
            sx={{
              color: 'text.secondary',
              p: 0.5,
              '&:hover': {
                backgroundColor: 'action.hover'
              }
            }}
          >
            {mode === 'dark' ? (
              <Brightness7Icon sx={{ fontSize: 20 }} />
            ) : (
              <Brightness4Icon sx={{ fontSize: 20 }} />
            )}
          </IconButton>

          <IconButton
            sx={{
              color: 'text.secondary',
              p: 0.5,
              '&:hover': {
                backgroundColor: 'action.hover'
              }
            }}
            disableRipple
          >
            <Avatar 
              sx={{ 
                width: 24, 
                height: 24,
                fontSize: '0.875rem',
                bgcolor: '#4c1298'
              }}
            >
              V
            </Avatar>
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
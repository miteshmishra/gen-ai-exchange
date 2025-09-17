import { AppBar, Toolbar, Typography, Avatar, Box, IconButton, Button } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

interface HeaderProps {
  onMenuClick: () => void;
  isMobile: boolean;
  isCollapsed?: boolean;
}

const Header = ({ onMenuClick, isMobile, isCollapsed = false }: HeaderProps) => {
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
          height: '50px',
          minHeight: '50px !important',
          py: '8px',
          backgroundImage: 'none',
          '&.MuiToolbar-root': {
            height: '50px',
            minHeight: '50px !important',
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

          <Box 
            sx={{ 
              display: 'flex',
              alignItems: 'center',
              ml: 1,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
              px: 0.5,
              py: 0.25,
              '&:hover': {
                bgcolor: 'action.hover',
                cursor: 'pointer'
              }
            }}
          >
            <Typography
              variant="body2"
              sx={{
                color: 'text.secondary',
                fontSize: '0.75rem',
              }}
            >
              2.5 Flash
            </Typography>
            <ArrowDropDownIcon sx={{ fontSize: 16, color: 'text.secondary', ml: 0.5 }} />
          </Box>
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
          <Button
            variant="contained"
            size="small"
            sx={{
              bgcolor: 'background.default',
              color: 'text.primary',
              textTransform: 'none',
              px: 1.5,
              py: 0.5,
              fontSize: '0.75rem',
              transition: theme => theme.transitions.create(['opacity', 'width', 'padding', 'margin'], {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.enteringScreen,
              }),
              '&:hover': {
                bgcolor: 'action.hover'
              }
            }}
          >
            Upgrade
          </Button>

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
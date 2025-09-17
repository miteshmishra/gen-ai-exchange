import { useState } from 'react';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import type { ReactNode } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { useChat } from '../../contexts/ChatContext';

const DRAWER_WIDTH = 280;
const COLLAPSED_DRAWER_WIDTH = 72;

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { messages } = useChat();

  const handleDrawerToggle = () => {
    if (isMobile) {
      setMobileOpen(!mobileOpen);
    } else {
      setIsCollapsed(!isCollapsed);
    }
  };

  const handleNewChat = () => {
    const { clearMessages } = useChat();
    clearMessages();
    if (isMobile) {
      handleDrawerToggle();
    }
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Header 
        onMenuClick={handleDrawerToggle}
        isMobile={isMobile}
        isCollapsed={!isMobile && isCollapsed}
      />
      
      <Sidebar
        open={isMobile ? mobileOpen : true}
        onClose={handleDrawerToggle}
        messages={messages}
        onNewChat={handleNewChat}
        width={DRAWER_WIDTH}
        variant={isMobile ? 'temporary' : 'permanent'}
        isCollapsed={!isMobile && isCollapsed}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: '100%',
          marginLeft: {
            xs: 0,
            sm: `${isCollapsed ? COLLAPSED_DRAWER_WIDTH : DRAWER_WIDTH}px`
          },
          mt: '32px', // Fixed header height
          height: 'calc(100vh - 32px)',
          overflow: 'hidden',
          transition: theme => theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          backgroundColor: 'background.default'
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
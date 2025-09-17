import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import ExploreIcon from '@mui/icons-material/Explore';
import ChatIcon from '@mui/icons-material/Chat';
import SettingsIcon from '@mui/icons-material/Settings';
import HelpIcon from '@mui/icons-material/Help';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import type { ChatMessage } from '../../types/chat';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  messages: ChatMessage[];
  onNewChat: () => void;
  width: number;
  variant: 'permanent' | 'temporary';
  isCollapsed?: boolean;
}

const Sidebar = ({ open, onClose, messages, onNewChat, width, variant, isCollapsed = false }: SidebarProps) => {
  // Group messages by conversation (for now, we'll just show the first message of each conversation)
  const conversations = messages.reduce((acc: { id: string; title: string }[], message) => {
    if (message.role === 'user') {
      const existingConversation = acc.find(conv => conv.id === message.id);
      if (!existingConversation) {
        acc.push({
          id: message.id,
          title: message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '')
        });
      }
    }
    return acc;
  }, []);

  return (
    <Drawer
      variant={variant}
      open={open}
      onClose={onClose}
      sx={{
        width: isCollapsed ? 72 : width,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        '& .MuiDrawer-paper': {
          width: isCollapsed ? 72 : width,
          boxSizing: 'border-box',
          bgcolor: 'background.paper',
          borderRight: '1px solid',
          borderColor: 'divider',
          transition: theme => theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          overflowX: 'hidden',
          '& .MuiListItemText-root': {
            opacity: isCollapsed ? 0 : 1,
            my: '10px',
            transition: theme => theme.transitions.create('opacity', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.enteringScreen,
            }),
          },
          '& .MuiListItemIcon-root': {
            minWidth: isCollapsed ? 'auto' : 24,
            mr: isCollapsed ? 0 : 1,
            justifyContent: isCollapsed ? 'center' : 'flex-start',
          }
        },
      }}
    >
            <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        height: '100%',
        pt: '7px'
      }}>
        <List sx={{ 
          py: 0,
          mb: isCollapsed ? 0 : 0.5
        }}>
          <ListItem 
            disablePadding 
            sx={{ 
              mb: isCollapsed ? 2 : 0.5,
              display: 'flex',
              justifyContent: isCollapsed ? 'center' : 'space-between'
            }}
          >
            <ListItemButton
              onClick={onClose}
              sx={{
                minHeight: 28,
                py: 0.5,
                px: 0.5,
                ml: isCollapsed ? 0.5 : 0,
                mr: 0.5,
                minWidth: isCollapsed ? 28 : 'auto',
                borderRadius: 1,
                justifyContent: 'center',
                '&:hover': {
                  backgroundColor: 'action.hover'
                }
              }}
            >
              <MenuIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
            </ListItemButton>
            {!isCollapsed && (
              <ListItemButton
                sx={{
                  minHeight: 28,
                  py: 0.5,
                  px: 1,
                  mx: 0.5,
                  minWidth: 28,
                  borderRadius: 1,
                  justifyContent: 'center',
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <SearchIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
              </ListItemButton>
            )}
          </ListItem>
        </List>
        <List sx={{ 
          py: 0,
          mb: isCollapsed ? 0 : 0.5
        }}>
          <ListItem disablePadding sx={{ mb: isCollapsed ? 2 : 0.5 }}>
            <ListItemButton
              onClick={onNewChat}
              sx={{
                minHeight: 28,
                py: 0.5,
                px: isCollapsed ? 0.5 : 1,
                mx: 0.5,
                borderRadius: 1,
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                '&:hover': {
                  backgroundColor: 'action.hover'
                }
              }}
            >
              <ListItemIcon>
                <AddIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
              </ListItemIcon>
              <ListItemText 
                primary="New chat"
                primaryTypographyProps={{
                  fontSize: '0.875rem',
                  color: 'text.primary'
                }}
                sx={{
                  m: 0,
                  display: isCollapsed ? 'none' : 'block'
                }}
              />
            </ListItemButton>
          </ListItem>
        </List>

        {!isCollapsed && (
          <Typography
            variant="overline"
            sx={{
              px: 2,
              py: 1,
              fontSize: '0.6875rem',
              fontWeight: 500,
              color: 'text.secondary',
              letterSpacing: '0.1em'
            }}
          >
            Gems
          </Typography>
        )}

        <List sx={{ 
          py: 0,
          '& .MuiListItem-root': {
            mb: isCollapsed ? 2 : 0.5,
            '&:last-child': {
              mb: 0
            }
          }
        }}>
          <ListItem disablePadding>
            <ListItemButton
              sx={{
                minHeight: 28,
                py: 0.5,
                px: isCollapsed ? 0.5 : 1,
                mx: 0.5,
                borderRadius: 1,
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                '&:hover': {
                  backgroundColor: 'action.hover'
                }
              }}
            >
              <ListItemIcon>
                <AutoStoriesIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
              </ListItemIcon>
              <ListItemText 
                primary="Storybook"
                primaryTypographyProps={{
                  noWrap: true,
                  fontSize: '0.875rem',
                  color: 'text.secondary'
                }}
                sx={{
                  m: 0,
                  display: isCollapsed ? 'none' : 'block'
                }}
              />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton
              sx={{
                minHeight: 28,
                py: 0.5,
                px: isCollapsed ? 0.5 : 1,
                mx: 0.5,
                borderRadius: 1,
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                '&:hover': {
                  backgroundColor: 'action.hover'
                }
              }}
            >
              <ListItemIcon>
                <ExploreIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
              </ListItemIcon>
              <ListItemText 
                primary="Explore Gems"
                primaryTypographyProps={{
                  noWrap: true,
                  fontSize: '0.875rem',
                  color: 'text.secondary'
                }}
                sx={{
                  m: 0,
                  display: isCollapsed ? 'none' : 'block'
                }}
              />
            </ListItemButton>
          </ListItem>
        </List>

        {!isCollapsed && (
          <Typography
            variant="overline"
            sx={{
              px: 2,
              py: 1,
              fontSize: '0.6875rem',
              fontWeight: 500,
              color: 'text.secondary',
              letterSpacing: '0.1em'
            }}
          >
            Recent
          </Typography>
        )}

        <List sx={{ 
          flex: 1, 
          overflow: 'auto', 
          py: 0,
          '& .MuiListItem-root': {
            mb: isCollapsed ? 2 : 0.5,
            '&:last-child': {
              mb: 0
            }
          }
        }}>
          {conversations.map((conversation) => (
            <ListItem key={conversation.id} disablePadding>
              <ListItemButton
                sx={{
                  minHeight: 28,
                  py: 0.5,
                  px: isCollapsed ? 0.5 : 1,
                  mx: 0.5,
                  borderRadius: 1,
                  justifyContent: isCollapsed ? 'center' : 'flex-start',
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ListItemIcon>
                  <ChatIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
                </ListItemIcon>
                <ListItemText 
                  primary={conversation.title}
                  primaryTypographyProps={{
                    noWrap: true,
                    fontSize: '0.875rem',
                    color: 'text.secondary'
                  }}
                  sx={{
                    m: 0,
                    display: isCollapsed ? 'none' : 'block'
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

        <Divider sx={{ my: 1, display: isCollapsed ? 'none' : 'block' }} />

        <List sx={{ 
          py: 0,
          '& .MuiListItem-root': {
            mb: isCollapsed ? 2 : 0.5,
            '&:last-child': {
              mb: 0
            }
          }
        }}>
          <ListItem disablePadding>
            <ListItemButton
              sx={{
                minHeight: 28,
                py: 0.5,
                px: isCollapsed ? 0.5 : 1,
                mx: 0.5,
                borderRadius: 1,
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                '&:hover': {
                  backgroundColor: 'action.hover'
                }
              }}
            >
              <ListItemIcon>
                <SettingsIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
              </ListItemIcon>
              <ListItemText 
                primary="Settings & Help"
                primaryTypographyProps={{
                  noWrap: true,
                  fontSize: '0.875rem',
                  color: 'text.secondary'
                }}
                sx={{
                  m: 0,
                  display: isCollapsed ? 'none' : 'block'
                }}
              />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
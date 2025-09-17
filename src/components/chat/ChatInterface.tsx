import { useState } from 'react';
import { 
  TextField, 
  Typography,
  Avatar,
  IconButton,
  Box,
  Stack,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import MicIcon from '@mui/icons-material/Mic';
import SendIcon from '@mui/icons-material/Send';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import StarIcon from '@mui/icons-material/Star';
import ShareIcon from '@mui/icons-material/Share';

const ChatInterface = () => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      // Handle sending message
      setMessage('');
    }
  };

  return (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        backgroundColor: 'background.default',
      }}
    >
      {/* Messages Area */}
      <Box 
        sx={{ 
          flex: 1,
          overflowY: 'auto',
          px: 3,
          py: 4,
          display: 'flex',
          flexDirection: 'column',
          gap: 4
        }}
      >
        {/* User Message */}
        <Stack
          direction="row"
          spacing={2}
          alignItems="flex-start"
          sx={{
            maxWidth: '800px',
            width: '100%',
            mx: 'auto',
            justifyContent: 'flex-end'
          }}
        >
          <Box sx={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
            <Box sx={{ maxWidth: '85%' }}>
              <Typography
                sx={{
                  color: 'text.primary',
                  fontSize: '0.875rem',
                  lineHeight: 1.5,
                  mb: 0.5
                }}
              >
                Hi
              </Typography>
            </Box>
          </Box>
          <Avatar
            sx={{
              width: 32,
              height: 32,
              bgcolor: '#4c1298',
              fontSize: '0.875rem'
            }}
          >
            V
          </Avatar>
        </Stack>

        {/* AI Message */}
        <Stack
          direction="row"
          spacing={2}
          alignItems="flex-start"
          sx={{
            maxWidth: '800px',
            width: '100%',
            mx: 'auto'
          }}
        >
          <StarIcon 
            sx={{ 
              color: 'primary.main',
              fontSize: 20,
              mt: 0.5
            }}
          />
          <Box sx={{ flex: 1 }}>
            <Typography
              sx={{
                color: 'text.primary',
                fontSize: '0.875rem',
                lineHeight: 1.5,
                mb: 1
              }}
            >
              Hello there! I'm here to help. What's on your mind?
            </Typography>
            <Stack 
              direction="row"
              spacing={1}
              sx={{ mt: 1 }}
            >
              <IconButton
                size="small"
                sx={{
                  color: 'text.secondary',
                  p: 0.5,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ContentCopyIcon sx={{ fontSize: 18 }} />
              </IconButton>
              <IconButton
                size="small"
                sx={{
                  color: 'text.secondary',
                  p: 0.5,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ThumbUpIcon sx={{ fontSize: 18 }} />
              </IconButton>
              <IconButton
                size="small"
                sx={{
                  color: 'text.secondary',
                  p: 0.5,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ThumbDownIcon sx={{ fontSize: 18 }} />
              </IconButton>
              <IconButton
                size="small"
                sx={{
                  color: 'text.secondary',
                  p: 0.5,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ShareIcon sx={{ fontSize: 18 }} />
              </IconButton>
              <IconButton
                size="small"
                sx={{
                  color: 'text.secondary',
                  p: 0.5,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <MoreVertIcon sx={{ fontSize: 18 }} />
              </IconButton>
            </Stack>
          </Box>
        </Stack>
      </Box>

      {/* Input Area */}
      <Box 
        sx={{ 
          position: 'sticky',
          bottom: 0,
          width: '100%',
          maxWidth: '1000px',
          mx: 'auto',
          p: 2,
          pb: 3,
          bgcolor: 'background.default'
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-end',
            gap: 1,
            bgcolor: 'background.paper',
            borderRadius: 2,
            p: 0.75,
            minHeight: '56px',
            border: '1px solid',
            borderColor: 'divider'
          }}
        >
          <IconButton
            size="small"
            sx={{
              color: 'text.secondary',
              p: 1,
              '&:hover': {
                bgcolor: 'action.hover'
              }
            }}
          >
            <AddIcon sx={{ fontSize: 20 }} />
          </IconButton>
          
          <TextField
            fullWidth
            multiline
            maxRows={7}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask Gemini..."
            variant="standard"
            sx={{
              flex: 1,
              '& .MuiInputBase-root': {
                px: 1,
                py: 0.5,
                fontSize: '1rem',
                '&::before, &::after': {
                  display: 'none'
                }
              }
            }}
          />

          <Box sx={{ display: 'flex', gap: 0.5 }}>
            <IconButton
              size="small"
              sx={{
                color: 'text.secondary',
                p: 1,
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <MicIcon sx={{ fontSize: 20 }} />
            </IconButton>
            <IconButton
              size="small"
              onClick={handleSend}
              sx={{
                color: 'text.secondary',
                p: 1,
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <SendIcon sx={{ fontSize: 20 }} />
            </IconButton>
          </Box>
        </Box>
        <Typography
          variant="caption"
          sx={{
            display: 'block',
            textAlign: 'center',
            mt: 1,
            color: 'text.secondary',
            fontSize: '0.75rem'
          }}
        >
          Gemini can make mistakes. Consider double-check it
        </Typography>
      </Box>
    </Box>
  );
};

export default ChatInterface;
import { useState } from 'react';
import type { KeyboardEvent } from 'react';
import { Box, Paper, InputBase, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isProcessing: boolean;
}

const ChatInput = ({ onSendMessage, isProcessing }: ChatInputProps) => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !isProcessing) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: 0,
        right: 0,
        left: {
          xs: 0,
          sm: `${72}px`, // COLLAPSED_DRAWER_WIDTH
          md: `${280}px`, // DRAWER_WIDTH
        },
        bgcolor: 'background.default',
        p: 2,
        pb: 3,
        transition: theme => theme.transitions.create('left', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
        }),
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: '8px 16px',
          display: 'flex',
          alignItems: 'center',
          width: '100%',
          borderRadius: 3,
          bgcolor: 'background.paper',
        }}
      >
      <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder="Ask about your trip plans..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        multiline
        maxRows={4}
        disabled={isProcessing}
      />
      <IconButton
        color="primary"
        sx={{ p: '10px' }}
        onClick={handleSend}
        disabled={!message.trim() || isProcessing}
      >
        {isProcessing ? (
          <CircularProgress size={24} />
        ) : (
          <SendIcon />
        )}
      </IconButton>
    </Paper>
    </Box>
  );
};

export default ChatInput;
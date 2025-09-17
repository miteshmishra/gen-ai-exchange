import { useState } from 'react';
import type { KeyboardEvent } from 'react';
import { Paper, InputBase, IconButton, CircularProgress } from '@mui/material';
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
    <Paper
      elevation={3}
      sx={{
        p: '8px 16px',
        display: 'flex',
        alignItems: 'center',
        position: 'sticky',
        bottom: 16,
        mx: 2,
        borderRadius: 3,
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
  );
};

export default ChatInput;
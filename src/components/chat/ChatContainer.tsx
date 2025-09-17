import { useRef, useEffect } from 'react';
import { Box } from '@mui/material';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { useChat } from '../../contexts/ChatContext';

const ChatContainer = () => {
  const { messages, isProcessing, addMessage, setProcessing, activeConversationId } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const messagesToShow = activeConversationId 
    ? messages.filter(m => m.id === activeConversationId || m.id.startsWith(activeConversationId + '-'))
    : messages;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    addMessage(content, 'user');
    setProcessing(true);

    // TODO: Implement AI processing here
    // Simulated response for now
    setTimeout(() => {
      addMessage('I can help you plan your trip. What kind of destination are you interested in?', 'assistant');
      setProcessing(false);
    }, 1000);
  };

  return (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.default',
        width: '100%',
      }}
    >
      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          pb: 20, // Add padding to prevent content from being hidden behind input
          width: '100%',
          maxWidth: '900px',
          mx: 'auto',
          px: { xs: 2, sm: 3, md: 4 }
        }}
      >
        {messagesToShow.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </Box>
      <ChatInput onSendMessage={handleSendMessage} isProcessing={isProcessing} />
    </Box>
  );
};

export default ChatContainer;
import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { ChatMessage, ChatState } from '../types/chat';

interface ChatContextType extends ChatState {
  addMessage: (content: string, role: ChatMessage['role']) => void;
  setProcessing: (isProcessing: boolean) => void;
  clearMessages: () => void;
  activeConversationId: string | null;
  setActiveConversationId: (id: string | null) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);

  const addMessage = (content: string, role: ChatMessage['role']) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      role,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const clearMessages = () => {
    setMessages([]);
    setActiveConversationId(null);
  };

  const setProcessing = (processing: boolean) => {
    setIsProcessing(processing);
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        isProcessing,
        addMessage,
        setProcessing,
        clearMessages,
        activeConversationId,
        setActiveConversationId,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export default ChatContext;
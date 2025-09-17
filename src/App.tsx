import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import theme from './theme/theme';
import ChatContainer from './components/chat/ChatContainer';
import Layout from './components/layout/Layout';
import { ChatProvider } from './contexts/ChatContext';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ChatProvider>
        <Layout>
          <ChatContainer />
        </Layout>
      </ChatProvider>
    </ThemeProvider>
  )
}

export default App

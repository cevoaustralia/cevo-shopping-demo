import { StrictMode } from 'react'
import * as ReactDOMClient from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import { ThemeProvider } from 'commons/style/styled-components'
import { theme } from 'commons/style/theme'
import GlobalStyle from 'commons/style/global-style'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

/* Context Providers */
import { CartProvider } from 'contexts/cart-context'

import App from 'components/App'

const root = document.getElementById('root')!
const container = ReactDOMClient.createRoot(root)
const queryClient = new QueryClient()

container.render(
    <QueryClientProvider client={queryClient}>
        <StrictMode>
            <ThemeProvider theme={theme}>
                <GlobalStyle />
                    <BrowserRouter>
                        <CartProvider>
                            <App />
                        </CartProvider>
                    </BrowserRouter>
            </ThemeProvider>
        </StrictMode>
        <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
)

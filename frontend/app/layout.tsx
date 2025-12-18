import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: 'RAG Q&A Chatbot',
    description: 'AI Agent Chatbot with RAG',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}

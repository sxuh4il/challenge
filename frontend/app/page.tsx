"use client";

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from './Chat.module.css';

type Message = {
    role: 'user' | 'ai';
    content: string;
    sources?: string[];
};

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: userMessage }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to fetch response');
            }

            const data = await response.json();

            console.log("Réponse du backend:", data);

            setMessages(prev => [...prev, {
                role: 'ai',
                content: data.result || data.answer || "Pas de réponse reçue.",
                sources: data.source_documents
                    ? data.source_documents.map((doc: any) => doc.metadata.source || "Source inconnue")
                    : (data.sources || [])
            }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'ai',
                content: `Error: ${error instanceof Error ? error.message : 'Something went wrong. Please check if the backend is running and documents are ingested.'}`
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className={styles.container}>
            <header className={styles.header}>
                <h1 className={styles.title}>Quorium RAG Assistant</h1>
            </header>

            <div className={styles.chatWindow}>
                {messages.length === 0 && (
                    <div className={styles.message} style={{ alignSelf: 'center', color: '#94a3b8', background: 'transparent', textAlign: 'center' }}>
                        <p>Welcome! Ask me anything about your documents.</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.aiMessage}`}
                    >
                        <div className="prose prose-invert max-w-none">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>

                        {msg.role === 'ai' && msg.sources && msg.sources.length > 0 && (
                            <div className={styles.sources}>
                                <div className={styles.sourceTitle}>Sources:</div>
                                <div className={styles.sourceList}>
                                    {msg.sources.map((src, i) => (
                                        <span key={i} className={styles.sourceItem}>{src}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                ))}

                {isLoading && (
                    <div className={`${styles.message} ${styles.aiMessage}`}>
                        <div className={styles.loading}>
                            Thinking<span className={styles.dot}></span><span className={styles.dot}></span><span className={styles.dot}></span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className={styles.inputArea}>
                <form onSubmit={handleSubmit} className={styles.form}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your question..."
                        className={styles.input}
                        disabled={isLoading}
                    />
                    <button type="submit" className={styles.submitButton} disabled={isLoading || !input.trim()}>
                        Send
                    </button>
                </form>
            </div>
        </main>
    );
}

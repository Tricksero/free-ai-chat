"use client"

import React, { DOMElement, ReactHTMLElement, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Todo } from "@/app/page";
import useWebSocket from "react-use-websocket";


function createSocketURL(roomName: string): string {
    var host = "localhost:8000"
    const socketpath = 'ws://' + host + '/ws/api/' + roomName + '/'
    return socketpath
}

const Page: React.FC<any> = ({ params }) => {
    const { sendMessage, lastMessage, readyState } = useWebSocket(createSocketURL(params.room_name));

    const router = useRouter();
    const [messages, setMessages] = useState<string[]>([]);
    const messageDisplay = useRef<HTMLDivElement>(null)
    const chatInput = useRef<HTMLInputElement>(null)
    const messageClasses = "m-4 bg-slate-300"

    const onClickSend = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        sendMessage(JSON.stringify({
            'message': (chatInput.current as HTMLInputElement).value
        }));
        (chatInput.current as HTMLInputElement).value = ""
    }

    useEffect(() => {
        if (lastMessage !== null) {
            const message = JSON.parse(lastMessage.data);
            console.log('Received message:', message.message);
            setMessages([...messages, message.message]) 
            return
        }
    }, [lastMessage]);
    
    return (
        <div className="w-10/12 flex flex-col">
            <div>WebSocket state: {readyState}</div>
            <div className="flex flex-col" ref={messageDisplay}>
                {messages.map((message:string, index: number) => (
                    <p key={index} className={messageClasses}>
                        {message}
                    </p>
                ))}
            </div>
            <div className="flex flex-row">
                <div className="flex flex-col">
                    <label htmlFor="chat-input">Type Message</label>
                    <input id="chat-input" ref={chatInput} type="text" />
                </div>
                <button onClick={onClickSend}>
                    Send</button>
            </div>
        </div>
    );
};

export default Page;
import { useRef, useEffect } from "react";
import { ChatUser, Message } from "../chatServiceClient/generatedProtos/chat_service";
import ChatBubble from "./ChatBubble";

function MessageBox({
	user,
	messageList,
}: {
	user: ChatUser;
	messageList: Array<Message>;
}) {
	const outerRef = useRef<HTMLDivElement>(null);
	const innerRef = useRef<HTMLDivElement>(null);
    const prevInnerDivHeight = useRef<number>(0);

	useEffect(() => {
		if (outerRef.current && innerRef.current) {
			const outerHeight = outerRef.current.clientHeight;
			const innerHeight = innerRef.current.clientHeight;
            const outerDivScrollTop = outerRef.current.scrollTop;

            if (!prevInnerDivHeight.current || outerDivScrollTop === prevInnerDivHeight.current - outerHeight) {
                outerRef.current.scrollTo({
                    top: innerHeight - outerHeight,
                    behavior: "smooth",
                    left: 0,
                });
            };

            prevInnerDivHeight.current = innerHeight;
		}
	}, [messageList]);

	return (
		<div
			ref={outerRef}
			className="card py-5 px-5 h-[66vh] w-[66vw] bg-primary shadow-lg overflow-scroll flex-col-reverse no-scrollbar"
		>
			<div ref={innerRef} className="relative">
				{messageList.map((message, index) => (
					<ChatBubble key={index} user={user} message={message} />
				))}
			</div>
		</div>
	);
}

export default MessageBox;

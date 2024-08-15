function ConnectionStatusBanner({
	connectionStatus,
	conversationID,
}: {
	connectionStatus: boolean;
	conversationID: string;
}) {
	return (
		<div>
			{connectionStatus ? (
				<div className="card p-5 mb-5 bg-success">
					<h2>You are connected to: {conversationID}</h2>
				</div>
			) : (
				<div className="card p-5 mb-5 bg-warning">
					<h2>You are not connected</h2>
				</div>
			)}
		</div>
	);
}

export default ConnectionStatusBanner;

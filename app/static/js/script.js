let fetching = false; // Flag to prevent concurrent requests

function formatAssetPositions(assetPositions) {
    let positionsHtml = '';

    // Iterate over each assetPosition
    assetPositions.forEach(item => {
        const position = item.position;
        positionsHtml += `<tr>
                            <td>${position.coin}</td>
                            <td>${position.entryPx || 'N/A'}</td>
                            <td>${position.unrealizedPnl}</td>
                          </tr>`;
    });

    return positionsHtml;
}

async function fetchStateChanges() {
    if (fetching) {
        return; // Already fetching, skip this request
    }
    fetching = true; // Set fetching flag to true

    try {
        const response = await fetch('/state_changes');
        const data = await response.json();

        let feedHtml = '';

        // Iterate over each user state change
        for (const [address, changes] of Object.entries(data)) {
            // Update the wallet address
            const walletAddressElement = document.getElementById('wallet-address');
            if (walletAddressElement) {
                walletAddressElement.textContent = `Address: ${address}`;
            }

            feedHtml += `<div class="container mt-4">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Coin</th>
                                        <th>Entry Price</th>
                                        <th>Unrealized PNL</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${formatAssetPositions(changes.assetPositions)}
                                </tbody>
                            </table>
                         </div>`;
        }

        const tablePlaceholder = document.getElementById('table-placeholder');
        if (feedHtml) {
            tablePlaceholder.innerHTML = feedHtml;
        } else {
            tablePlaceholder.innerHTML = '<p>No new changes.</p>';
        }
        
    } catch (error) {
        console.error('Error fetching state changes:', error);
        tablePlaceholder.innerHTML = '<p>Error loading state changes.</p>';
    } finally {
        fetching = false; // Reset fetching flag after the request is completed
    }
}

setInterval(fetchStateChanges, 5000); // Fetch state changes every 5 seconds
fetchStateChanges(); // Initial fetch

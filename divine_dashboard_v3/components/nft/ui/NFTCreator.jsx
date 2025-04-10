import React, { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Card, Button, Form, Alert, Spinner, ProgressBar } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock, faShieldAlt, faFingerprint, faCheck, faTimes, faRandom } from '@fortawesome/free-solid-svg-icons';

// Import blockchain interface
const BlockchainInterface = require('../utils/blockchain_interface');

/**
 * NFT Creator component for creating quantum-secured NFTs
 */
const NFTCreator = () => {
    // State for NFT creation form
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState('');
    const [attributes, setAttributes] = useState([{ trait_type: '', value: '' }]);
    const [loading, setLoading] = useState(false);
    const [alert, setAlert] = useState({ show: false, variant: '', message: '' });
    const [mintingStep, setMintingStep] = useState(0);
    const [mintingProgress, setMintingProgress] = useState(0);

    // State for wallet connection
    const [walletConnected, setWalletConnected] = useState(false);
    const [walletAddress, setWalletAddress] = useState('');
    const [network, setNetwork] = useState('');

    // State for quantum security
    const [quantumHashes, setQuantumHashes] = useState([]);
    const [selectedHash, setSelectedHash] = useState('');
    const [securityLevel, setSecurityLevel] = useState(0);
    const [entropyCollected, setEntropyCollected] = useState(false);

    // Blockchain interface instance
    const blockchainInterface = useRef(new BlockchainInterface());

    // Effect to check connection status on component mount
    useEffect(() => {
        const checkConnection = async () => {
            try {
                const status = blockchainInterface.current.getConnectionStatus();
                if (status.isConnected) {
                    setWalletConnected(true);
                    setWalletAddress(status.walletAddress);
                    setNetwork(status.network);
                    await fetchQuantumHashes();
                }
            } catch (error) {
                console.error('Error checking connection:', error);
            }
        };

        checkConnection();

        // Set up event listeners
        blockchainInterface.current.on('connect', handleConnect);
        blockchainInterface.current.on('disconnect', handleDisconnect);
        blockchainInterface.current.on('error', handleError);

        // Clean up event listeners
        return () => {
            blockchainInterface.current.off('connect', handleConnect);
            blockchainInterface.current.off('disconnect', handleDisconnect);
            blockchainInterface.current.off('error', handleError);
        };
    }, []);

    // Fetch available quantum hashes
    const fetchQuantumHashes = async () => {
        try {
            const hashes = await blockchainInterface.current.getAvailableQuantumHashes();
            setQuantumHashes(hashes);
            if (hashes.length > 0) {
                setSelectedHash(hashes[0].hash);
            }
        } catch (error) {
            console.error('Error fetching quantum hashes:', error);
            showAlert('danger', 'Failed to fetch quantum hashes. Please try again.');
        }
    };

    // Handle wallet connection
    const connectWallet = async () => {
        try {
            setLoading(true);
            const address = await blockchainInterface.current.connect();
            setWalletConnected(true);
            setWalletAddress(address);
            showAlert('success', 'Wallet connected successfully!');
            await fetchQuantumHashes();
        } catch (error) {
            console.error('Error connecting wallet:', error);
            showAlert('danger', `Failed to connect wallet: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // Handle wallet disconnection
    const disconnectWallet = () => {
        blockchainInterface.current.disconnect();
        setWalletConnected(false);
        setWalletAddress('');
        setNetwork('');
        showAlert('info', 'Wallet disconnected.');
    };

    // Handle wallet connection event
    const handleConnect = (data) => {
        setWalletConnected(true);
        setWalletAddress(data.address);
        setNetwork(data.network);
        fetchQuantumHashes();
    };

    // Handle wallet disconnection event
    const handleDisconnect = () => {
        setWalletConnected(false);
        setWalletAddress('');
        setNetwork('');
    };

    // Handle error event
    const handleError = (data) => {
        showAlert('danger', `Error: ${data.message}`);
    };

    // Display alert message
    const showAlert = (variant, message) => {
        setAlert({ show: true, variant, message });
        setTimeout(() => setAlert({ show: false, variant: '', message: '' }), 5000);
    };

    // Handle image upload
    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreviewUrl(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    // Handle attribute changes
    const handleAttributeChange = (index, field, value) => {
        const newAttributes = [...attributes];
        newAttributes[index][field] = value;
        setAttributes(newAttributes);
    };

    // Add new attribute field
    const addAttribute = () => {
        setAttributes([...attributes, { trait_type: '', value: '' }]);
    };

    // Remove attribute field
    const removeAttribute = (index) => {
        const newAttributes = attributes.filter((_, i) => i !== index);
        setAttributes(newAttributes);
    };

    // Simulate entropy collection for quantum security
    const collectEntropy = () => {
        setLoading(true);
        setMintingStep(1);

        // Simulate progressive entropy collection
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.floor(Math.random() * 10) + 1;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setEntropyCollected(true);
                setSecurityLevel(Math.floor(Math.random() * 3) + 3); // 3-5 security level
                setLoading(false);
                setMintingStep(2);
            }
            setMintingProgress(progress);
        }, 200);
    };

    // Handle NFT creation and minting
    const createNFT = async (e) => {
        e.preventDefault();

        if (!walletConnected) {
            showAlert('warning', 'Please connect your wallet first.');
            return;
        }

        if (!name || !description || !image) {
            showAlert('warning', 'Please fill all required fields.');
            return;
        }

        if (!selectedHash) {
            showAlert('warning', 'Please select a quantum hash for security.');
            return;
        }

        if (!entropyCollected) {
            collectEntropy();
            return;
        }

        try {
            setLoading(true);
            setMintingStep(3);

            // Upload image to IPFS (simulated)
            setMintingProgress(25);
            await simulateDelay(1000);
            const imageUri = 'ipfs://QmExample/image.png'; // Mock IPFS URI

            // Prepare metadata
            const filteredAttributes = attributes.filter(attr => attr.trait_type && attr.value);
            const metadata = {
                name,
                description,
                image: imageUri,
                attributes: [
                    ...filteredAttributes,
                    {
                        trait_type: 'Quantum Security Level',
                        value: securityLevel
                    }
                ],
                quantum_properties: {
                    hash: selectedHash,
                    timestamp: new Date().toISOString()
                }
            };

            // Upload metadata to IPFS (simulated)
            setMintingProgress(50);
            await simulateDelay(1000);
            const metadataUri = 'ipfs://QmExample/metadata.json'; // Mock IPFS URI

            // Mint NFT with quantum security
            setMintingProgress(75);
            const result = await blockchainInterface.current.mintNFT({
                tokenURI: metadataUri,
                quantumHash: selectedHash
            });

            setMintingProgress(100);
            setMintingStep(4);

            showAlert('success', `NFT minted successfully! Token ID: ${result.tokenId}`);

            // Reset form
            setName('');
            setDescription('');
            setImage(null);
            setPreviewUrl('');
            setAttributes([{ trait_type: '', value: '' }]);
            setEntropyCollected(false);
            setSecurityLevel(0);
            setMintingStep(0);
            setMintingProgress(0);
        } catch (error) {
            console.error('Error creating NFT:', error);
            showAlert('danger', `Failed to create NFT: ${error.message}`);
            setMintingStep(0);
            setMintingProgress(0);
        } finally {
            setLoading(false);
        }
    };

    // Utility function to simulate delay
    const simulateDelay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Render security level indicator
    const renderSecurityLevel = () => {
        if (securityLevel === 0) return null;

        const levels = [];
        for (let i = 0; i < 5; i++) {
            levels.push(
                <div
                    key={i}
                    className={`security-level-bar ${i < securityLevel ? 'active' : ''}`}
                />
            );
        }

        return (
            <div className="security-level-container">
                <span>Quantum Security Level: </span>
                <div className="security-level-bars">{levels}</div>
            </div>
        );
    };

    return (
        <Container className="nft-creator-container py-4">
            {alert.show && (
                <Alert variant={alert.variant} dismissible onClose={() => setAlert({ show: false })}>
                    {alert.message}
                </Alert>
            )}

            <Card className="mb-4">
                <Card.Header className="bg-dark text-white">
                    <h3 className="mb-0">
                        <FontAwesomeIcon icon={faShieldAlt} className="me-2" />
                        Quantum-Secure NFT Creator
                    </h3>
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col md={6} className="mb-4 mb-md-0">
                            <Card className="shadow-sm h-100">
                                <Card.Body>
                                    <h4 className="mb-3">Wallet Connection</h4>
                                    {walletConnected ? (
                                        <div>
                                            <div className="d-flex align-items-center mb-3">
                                                <div className="wallet-indicator connected me-2"></div>
                                                <span>Connected to {network}</span>
                                            </div>
                                            <p className="text-muted wallet-address">
                                                {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}
                                            </p>
                                            <Button
                                                variant="outline-danger"
                                                onClick={disconnectWallet}
                                                disabled={loading}
                                            >
                                                Disconnect Wallet
                                            </Button>
                                        </div>
                                    ) : (
                                        <div className="text-center">
                                            <p className="mb-3">Connect your wallet to create and mint NFTs</p>
                                            <Button
                                                variant="primary"
                                                size="lg"
                                                onClick={connectWallet}
                                                disabled={loading}
                                            >
                                                {loading ? (
                                                    <>
                                                        <Spinner
                                                            as="span"
                                                            animation="border"
                                                            size="sm"
                                                            role="status"
                                                            aria-hidden="true"
                                                            className="me-2"
                                                        />
                                                        Connecting...
                                                    </>
                                                ) : (
                                                    <>
                                                        <FontAwesomeIcon icon={faLock} className="me-2" />
                                                        Connect Wallet
                                                    </>
                                                )}
                                            </Button>
                                        </div>
                                    )}
                                </Card.Body>
                            </Card>
                        </Col>

                        <Col md={6}>
                            <Card className="shadow-sm h-100">
                                <Card.Body>
                                    <h4 className="mb-3">Quantum Security</h4>
                                    {walletConnected ? (
                                        <div>
                                            <Form.Group className="mb-3">
                                                <Form.Label>Select Quantum Hash</Form.Label>
                                                <Form.Select
                                                    value={selectedHash}
                                                    onChange={(e) => setSelectedHash(e.target.value)}
                                                    disabled={loading || quantumHashes.length === 0}
                                                >
                                                    {quantumHashes.length === 0 && (
                                                        <option value="">No quantum hashes available</option>
                                                    )}
                                                    {quantumHashes.map((hash, index) => (
                                                        <option key={index} value={hash.hash}>
                                                            {hash.hash.slice(0, 18)}...{hash.hash.slice(-6)} ({new Date(hash.timestamp).toLocaleDateString()})
                                                        </option>
                                                    ))}
                                                </Form.Select>
                                            </Form.Group>

                                            {entropyCollected ? (
                                                <div>
                                                    {renderSecurityLevel()}
                                                    <div className="d-flex align-items-center mt-3">
                                                        <FontAwesomeIcon icon={faCheck} className="text-success me-2" />
                                                        <span>Entropy collected successfully</span>
                                                    </div>
                                                </div>
                                            ) : (
                                                <Button
                                                    variant="outline-primary"
                                                    className="w-100"
                                                    onClick={collectEntropy}
                                                    disabled={loading || !selectedHash || quantumHashes.length === 0}
                                                >
                                                    <FontAwesomeIcon icon={faFingerprint} className="me-2" />
                                                    Collect Quantum Entropy
                                                </Button>
                                            )}
                                        </div>
                                    ) : (
                                        <div className="text-center text-muted">
                                            <FontAwesomeIcon icon={faLock} size="2x" className="mb-3" />
                                            <p>Connect your wallet to access quantum security features</p>
                                        </div>
                                    )}
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>

            <Form onSubmit={createNFT}>
                <Card className="mb-4">
                    <Card.Header className="bg-light">
                        <h4 className="mb-0">NFT Details</h4>
                    </Card.Header>
                    <Card.Body>
                        <Row>
                            <Col md={7}>
                                <Form.Group className="mb-3">
                                    <Form.Label>Name *</Form.Label>
                                    <Form.Control
                                        type="text"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        placeholder="Enter NFT name"
                                        disabled={loading}
                                        required
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Description *</Form.Label>
                                    <Form.Control
                                        as="textarea"
                                        rows={4}
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        placeholder="Describe your NFT"
                                        disabled={loading}
                                        required
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Image *</Form.Label>
                                    <Form.Control
                                        type="file"
                                        accept="image/*"
                                        onChange={handleImageChange}
                                        disabled={loading}
                                        required={!image}
                                    />
                                </Form.Group>
                            </Col>

                            <Col md={5}>
                                <div className="mb-3">
                                    <label className="form-label">Preview</label>
                                    <div className="nft-preview-container">
                                        {previewUrl ? (
                                            <img
                                                src={previewUrl}
                                                alt="NFT Preview"
                                                className="img-fluid rounded"
                                            />
                                        ) : (
                                            <div className="nft-preview-placeholder d-flex align-items-center justify-content-center">
                                                <span className="text-muted">Image Preview</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>

                <Card className="mb-4">
                    <Card.Header className="bg-light">
                        <h4 className="mb-0">NFT Attributes</h4>
                    </Card.Header>
                    <Card.Body>
                        {attributes.map((attr, index) => (
                            <Row key={index} className="mb-3">
                                <Col sm={5}>
                                    <Form.Control
                                        type="text"
                                        placeholder="Trait name"
                                        value={attr.trait_type}
                                        onChange={(e) => handleAttributeChange(index, 'trait_type', e.target.value)}
                                        disabled={loading}
                                    />
                                </Col>
                                <Col sm={5}>
                                    <Form.Control
                                        type="text"
                                        placeholder="Value"
                                        value={attr.value}
                                        onChange={(e) => handleAttributeChange(index, 'value', e.target.value)}
                                        disabled={loading}
                                    />
                                </Col>
                                <Col sm={2}>
                                    <Button
                                        variant="outline-danger"
                                        onClick={() => removeAttribute(index)}
                                        disabled={loading || attributes.length <= 1}
                                        className="w-100"
                                    >
                                        <FontAwesomeIcon icon={faTimes} />
                                    </Button>
                                </Col>
                            </Row>
                        ))}

                        <Button
                            variant="outline-secondary"
                            onClick={addAttribute}
                            disabled={loading}
                            className="mt-2"
                        >
                            Add Attribute
                        </Button>
                    </Card.Body>
                </Card>

                {mintingStep > 0 && (
                    <Card className="mb-4">
                        <Card.Header className="bg-light">
                            <h4 className="mb-0">Minting Progress</h4>
                        </Card.Header>
                        <Card.Body>
                            <ProgressBar now={mintingProgress} label={`${mintingProgress}%`} className="mb-3" />

                            <div className="d-flex justify-content-between">
                                <div className={`step-indicator ${mintingStep >= 1 ? 'active' : ''}`}>
                                    <div className="step-number">1</div>
                                    <div className="step-label">Entropy Collection</div>
                                </div>
                                <div className={`step-indicator ${mintingStep >= 2 ? 'active' : ''}`}>
                                    <div className="step-number">2</div>
                                    <div className="step-label">Security Validation</div>
                                </div>
                                <div className={`step-indicator ${mintingStep >= 3 ? 'active' : ''}`}>
                                    <div className="step-number">3</div>
                                    <div className="step-label">Upload to IPFS</div>
                                </div>
                                <div className={`step-indicator ${mintingStep >= 4 ? 'active' : ''}`}>
                                    <div className="step-number">4</div>
                                    <div className="step-label">Blockchain Minting</div>
                                </div>
                            </div>
                        </Card.Body>
                    </Card>
                )}

                <div className="d-grid">
                    <Button
                        type="submit"
                        variant="primary"
                        size="lg"
                        disabled={loading || !walletConnected}
                    >
                        {loading ? (
                            <>
                                <Spinner
                                    as="span"
                                    animation="border"
                                    size="sm"
                                    role="status"
                                    aria-hidden="true"
                                    className="me-2"
                                />
                                {mintingStep === 1 ? 'Collecting Entropy...' :
                                    mintingStep === 2 ? 'Validating Security...' :
                                        mintingStep === 3 ? 'Creating NFT...' :
                                            mintingStep === 4 ? 'Finalizing...' : 'Processing...'}
                            </>
                        ) : entropyCollected ? (
                            <>
                                <FontAwesomeIcon icon={faShieldAlt} className="me-2" />
                                Create Quantum-Secured NFT
                            </>
                        ) : (
                            <>
                                <FontAwesomeIcon icon={faFingerprint} className="me-2" />
                                Begin Quantum Security Process
                            </>
                        )}
                    </Button>
                </div>
            </Form>

            <style jsx>{`
        .nft-creator-container {
          max-width: 900px;
          margin: 0 auto;
        }
        
        .nft-preview-container {
          height: 200px;
          border: 2px dashed #dee2e6;
          border-radius: 0.25rem;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .nft-preview-container img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
        
        .wallet-indicator {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background-color: #28a745;
        }
        
        .wallet-address {
          font-family: monospace;
          background-color: #f8f9fa;
          padding: 5px 10px;
          border-radius: 4px;
          display: inline-block;
          margin-bottom: 10px;
        }
        
        .security-level-container {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
        }
        
        .security-level-bars {
          display: flex;
          margin-left: 10px;
        }
        
        .security-level-bar {
          width: 20px;
          height: 10px;
          margin-right: 3px;
          background-color: #e9ecef;
          border-radius: 2px;
        }
        
        .security-level-bar.active {
          background-color: #28a745;
        }
        
        .step-indicator {
          display: flex;
          flex-direction: column;
          align-items: center;
          width: 100px;
        }
        
        .step-number {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          background-color: #e9ecef;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 5px;
          font-weight: bold;
        }
        
        .step-indicator.active .step-number {
          background-color: #007bff;
          color: white;
        }
        
        .step-label {
          font-size: 0.8rem;
          text-align: center;
        }
      `}</style>
        </Container>
    );
};

export default NFTCreator; 
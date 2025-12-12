const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = 'uploads/';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, uuidv4() + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 50 * 1024 * 1024 } // 50MB limit
});

// In-memory data storage (replace with database in production)
let users = [];
let listings = [];
let transactions = [];
let memberships = {
  basic: { name: 'Basic', price: 0, platformFee: 0.15 },
  premium: { name: 'Premium', price: 9.99, platformFee: 0.10 },
  pro: { name: 'Pro', price: 29.99, platformFee: 0.05 }
};

// Routes

// Get all listings
app.get('/api/listings', (req, res) => {
  res.json(listings);
});

// Get a specific listing
app.get('/api/listings/:id', (req, res) => {
  const listing = listings.find(l => l.id === req.params.id);
  if (!listing) {
    return res.status(404).json({ error: 'Listing not found' });
  }
  res.json(listing);
});

// Create a new listing
app.post('/api/listings', upload.single('file'), (req, res) => {
  try {
    const { title, description, price, category, sellerId } = req.body;
    
    if (!title || !description || !price || !req.file) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const listing = {
      id: uuidv4(),
      title,
      description,
      price: parseFloat(price),
      category: category || 'other',
      sellerId: sellerId || 'anonymous',
      fileName: req.file.filename,
      originalName: req.file.originalname,
      filePath: req.file.path,
      fileSize: req.file.size,
      mimeType: req.file.mimetype,
      createdAt: new Date().toISOString(),
      sales: 0
    };

    listings.push(listing);
    res.status(201).json(listing);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create listing' });
  }
});

// Purchase a listing
app.post('/api/purchase/:id', (req, res) => {
  const { buyerId, membershipType } = req.body;
  const listing = listings.find(l => l.id === req.params.id);

  if (!listing) {
    return res.status(404).json({ error: 'Listing not found' });
  }

  const membership = memberships[membershipType || 'basic'];
  const platformFee = listing.price * membership.platformFee;
  const sellerReceives = listing.price - platformFee;

  const transaction = {
    id: uuidv4(),
    listingId: listing.id,
    buyerId: buyerId || 'anonymous',
    sellerId: listing.sellerId,
    amount: listing.price,
    platformFee,
    sellerReceives,
    timestamp: new Date().toISOString()
  };

  transactions.push(transaction);
  listing.sales += 1;

  res.json({
    success: true,
    transaction,
    downloadUrl: `/api/download/${listing.id}`
  });
});

// Download purchased file
app.get('/api/download/:id', (req, res) => {
  const listing = listings.find(l => l.id === req.params.id);
  
  if (!listing) {
    return res.status(404).json({ error: 'Listing not found' });
  }

  // In production, verify purchase before allowing download
  res.download(listing.filePath, listing.originalName);
});

// Get membership types
app.get('/api/memberships', (req, res) => {
  res.json(memberships);
});

// Create/update user membership
app.post('/api/users/:userId/membership', (req, res) => {
  const { userId } = req.params;
  const { membershipType } = req.body;

  if (!memberships[membershipType]) {
    return res.status(400).json({ error: 'Invalid membership type' });
  }

  let user = users.find(u => u.id === userId);
  if (!user) {
    user = {
      id: userId,
      membershipType: 'basic',
      joinedAt: new Date().toISOString()
    };
    users.push(user);
  }

  user.membershipType = membershipType;
  user.membershipUpdatedAt = new Date().toISOString();

  res.json(user);
});

// Get user info
app.get('/api/users/:userId', (req, res) => {
  const user = users.find(u => u.id === req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// Get sales statistics
app.get('/api/stats', (req, res) => {
  const stats = {
    totalListings: listings.length,
    totalTransactions: transactions.length,
    totalRevenue: transactions.reduce((sum, t) => sum + t.amount, 0),
    totalPlatformFees: transactions.reduce((sum, t) => sum + t.platformFee, 0)
  };
  res.json(stats);
});

// Serve main page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Quanti-Badger Data Marketplace running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} to get started`);
});

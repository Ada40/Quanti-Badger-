# 🦡 Quanti-Badger - Data Marketplace

A place where users can scan their device and determine/dictate what data they want to sell. Users can monetize their personal data including receipts, emails, documents, images, videos, and more.

## Features

### For Sellers
- **Device Scanning**: Browse and select files from your device to list on the marketplace
- **File Selection**: Pick and choose exactly what files, pics, or videos you want to release
- **Custom Pricing**: Set your own price for each listing
- **Multiple Categories**: Organize data as receipts, emails, documents, images, videos, or other
- **Anonymous or Identified**: Choose to list anonymously or with your seller ID

### For Buyers
- **Browse Marketplace**: Explore data listings from other users
- **Sample Previews**: View descriptions and details before purchasing
- **Instant Download**: Immediate access to purchased files
- **Search & Filter**: Find specific types of data easily

### Platform Features
- **Membership Tiers**: Three membership levels with varying platform fees
  - **Basic** ($0/month): 15% platform fee
  - **Premium** ($9.99/month): 10% platform fee
  - **Pro** ($29.99/month): 5% platform fee
- **Statistics Dashboard**: Real-time metrics on listings, transactions, and revenue
- **Secure Transactions**: All purchases are tracked with unique transaction IDs

## Installation

### Prerequisites
- Node.js 14.x or higher
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Ada40/Quanti-Badger-.git
cd Quanti-Badger-
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

### Selling Your Data

1. Click on "Sell Your Data" in the navigation menu
2. Choose a file from your device (receipts, emails, documents, images, videos, etc.)
3. Fill in the listing details:
   - Title: Give your listing a descriptive name
   - Description: Explain what's included and why it's valuable
   - Category: Select the appropriate category
   - Price: Set your asking price in USD
   - Seller ID: Optionally provide your seller ID (leave blank for anonymous)
4. Click "List Item for Sale"
5. Your listing will appear in the marketplace immediately

### Buying Data

1. Browse the marketplace on the home page
2. Use search and filters to find specific types of data
3. Click "Details" to view more information about a listing
4. Click "Purchase" to buy the data
5. Confirm the purchase
6. The file will automatically download

### Managing Membership

1. Click on "Memberships" in the navigation menu
2. View the three available tiers and their benefits
3. Click "Upgrade Now" on your preferred tier
4. Confirm the membership change
5. Your new platform fee rate takes effect immediately

## Technology Stack

- **Backend**: Node.js with Express
- **File Uploads**: Multer
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Storage**: File system (in-memory data storage for demo; use database in production)

## Project Structure

```
Quanti-Badger-/
├── public/
│   ├── index.html      # Main HTML interface
│   ├── styles.css      # Styling
│   └── app.js          # Frontend JavaScript
├── uploads/            # Uploaded files (gitignored)
├── server.js           # Express server & API
├── package.json        # Dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Endpoints

### Listings
- `GET /api/listings` - Get all listings
- `GET /api/listings/:id` - Get a specific listing
- `POST /api/listings` - Create a new listing (multipart/form-data)
- `GET /api/download/:id` - Download a purchased file

### Transactions
- `POST /api/purchase/:id` - Purchase a listing

### Users & Memberships
- `GET /api/users/:userId` - Get user information
- `POST /api/users/:userId/membership` - Update user membership
- `GET /api/memberships` - Get all membership types

### Statistics
- `GET /api/stats` - Get platform statistics

## Security Considerations

⚠️ **Important**: This is a demonstration application. For production use, you should:

1. **Add rate limiting** to prevent abuse of file download and static file endpoints (currently flagged by CodeQL)
2. Add proper authentication and authorization
3. Use a database instead of in-memory storage
4. Implement payment processing (Stripe, PayPal, etc.)
5. Add file validation and virus scanning
6. Add HTTPS/SSL certificates
7. Implement proper session management
8. Add data encryption for sensitive information
9. Purchase verification is implemented, but should be enhanced with session-based tracking
10. Add content moderation

## Development

### Running in Development Mode

```bash
npm run dev
```

This will start the server with nodemon for automatic reloading.

### File Upload Limits

- Maximum file size: 50MB (configurable in server.js)
- All file types are accepted

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Quanti-Badger** - Your data, your choice, your profit! 🦡

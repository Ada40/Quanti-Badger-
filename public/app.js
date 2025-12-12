// Current user session
let currentUser = {
    id: localStorage.getItem('userId') || generateUserId(),
    membershipType: localStorage.getItem('membershipType') || 'basic'
};

// Save user ID
localStorage.setItem('userId', currentUser.id);
localStorage.setItem('membershipType', currentUser.membershipType);

// Generate unique user ID
function generateUserId() {
    return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Section navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Load section-specific data
    if (sectionId === 'marketplace') {
        loadListings();
    } else if (sectionId === 'stats') {
        loadStatistics();
    }
}

// Load all listings
async function loadListings() {
    try {
        const response = await fetch('/api/listings');
        const listings = await response.json();
        
        displayListings(listings);
    } catch (error) {
        console.error('Error loading listings:', error);
        document.getElementById('listingsContainer').innerHTML = 
            '<p class="placeholder">Error loading listings. Please try again.</p>';
    }
}

// Display listings
function displayListings(listings) {
    const container = document.getElementById('listingsContainer');
    
    if (listings.length === 0) {
        container.innerHTML = '<p class="placeholder">No listings available yet. Be the first to list your data!</p>';
        return;
    }
    
    container.innerHTML = listings.map(listing => `
        <div class="listing-card" data-category="${listing.category}">
            <div class="listing-header">
                <div>
                    <span class="listing-category">${listing.category}</span>
                    <h3>${escapeHtml(listing.title)}</h3>
                </div>
                <div class="listing-price">$${listing.price.toFixed(2)}</div>
            </div>
            <p class="listing-description">${escapeHtml(listing.description)}</p>
            <div class="listing-meta">
                <span>📦 ${formatFileSize(listing.fileSize)}</span>
                <span>💰 ${listing.sales} sales</span>
            </div>
            <div class="listing-actions">
                <button class="btn-primary" onclick="purchaseListing('${listing.id}')">Purchase</button>
                <button class="btn-secondary" onclick="viewDetails('${listing.id}')">Details</button>
            </div>
        </div>
    `).join('');
}

// Filter listings
function filterListings() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    const cards = document.querySelectorAll('.listing-card');
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('.listing-description').textContent.toLowerCase();
        const cardCategory = card.dataset.category;
        
        const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
        const matchesCategory = !category || cardCategory === category;
        
        if (matchesSearch && matchesCategory) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Upload form handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    
    // File preview
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) {
            filePreview.classList.remove('active');
            return;
        }
        
        filePreview.classList.add('active');
        
        let previewHtml = `
            <strong>Selected File:</strong><br>
            <strong>Name:</strong> ${escapeHtml(file.name)}<br>
            <strong>Size:</strong> ${formatFileSize(file.size)}<br>
            <strong>Type:</strong> ${file.type || 'Unknown'}
        `;
        
        // Show image preview if it's an image
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewHtml += `<br><img src="${e.target.result}" alt="Preview" style="max-height: 200px;">`;
                filePreview.innerHTML = previewHtml;
            };
            reader.readAsDataURL(file);
        } else {
            filePreview.innerHTML = previewHtml;
        }
    });
    
    // Form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const statusDiv = document.getElementById('uploadStatus');
        const submitBtn = uploadForm.querySelector('button[type="submit"]');
        
        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading...';
        
        try {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('title', document.getElementById('titleInput').value);
            formData.append('description', document.getElementById('descriptionInput').value);
            formData.append('category', document.getElementById('categoryInput').value);
            formData.append('price', document.getElementById('priceInput').value);
            formData.append('sellerId', document.getElementById('sellerIdInput').value || currentUser.id);
            
            const response = await fetch('/api/listings', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const listing = await response.json();
                statusDiv.className = 'status-message success active';
                statusDiv.innerHTML = `
                    ✅ <strong>Success!</strong> Your listing has been created.<br>
                    <small>Listing ID: ${listing.id}</small>
                `;
                uploadForm.reset();
                filePreview.classList.remove('active');
                
                // Switch to marketplace after 2 seconds
                setTimeout(() => {
                    document.querySelector('.nav-btn').click();
                }, 2000);
            } else {
                throw new Error('Upload failed');
            }
        } catch (error) {
            statusDiv.className = 'status-message error active';
            statusDiv.textContent = '❌ Error: Failed to create listing. Please try again.';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'List Item for Sale';
        }
    });
    
    // Load initial data
    loadListings();
});

// Purchase listing
async function purchaseListing(listingId) {
    const confirmation = confirm('Are you sure you want to purchase this listing?');
    if (!confirmation) return;
    
    try {
        const response = await fetch(`/api/purchase/${listingId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                buyerId: currentUser.id,
                membershipType: currentUser.membershipType
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(`✅ Purchase successful!\n\nTransaction ID: ${result.transaction.id}\nAmount: $${result.transaction.amount}\nPlatform Fee: $${result.transaction.platformFee.toFixed(2)}\n\nDownloading file...`);
            
            // Trigger download
            window.location.href = result.downloadUrl;
            
            // Refresh listings
            loadListings();
        } else {
            throw new Error('Purchase failed');
        }
    } catch (error) {
        alert('❌ Error: Failed to complete purchase. Please try again.');
    }
}

// View listing details
async function viewDetails(listingId) {
    try {
        const response = await fetch(`/api/listings/${listingId}`);
        const listing = await response.json();
        
        alert(`
📦 Listing Details

Title: ${listing.title}
Category: ${listing.category}
Price: $${listing.price}
Description: ${listing.description}

File Name: ${listing.originalName}
File Size: ${formatFileSize(listing.fileSize)}
Sales: ${listing.sales}
Created: ${new Date(listing.createdAt).toLocaleString()}
        `);
    } catch (error) {
        alert('❌ Error: Failed to load listing details.');
    }
}

// Select membership
async function selectMembership(type) {
    if (type === currentUser.membershipType) {
        alert('You already have this membership level.');
        return;
    }
    
    const memberships = {
        basic: { name: 'Basic', price: 0 },
        premium: { name: 'Premium', price: 9.99 },
        pro: { name: 'Pro', price: 29.99 }
    };
    
    const selected = memberships[type];
    const message = selected.price > 0 
        ? `Upgrade to ${selected.name} for $${selected.price}/month?`
        : `Switch to ${selected.name} membership?`;
    
    if (!confirm(message)) return;
    
    try {
        const response = await fetch(`/api/users/${currentUser.id}/membership`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                membershipType: type
            })
        });
        
        if (response.ok) {
            currentUser.membershipType = type;
            localStorage.setItem('membershipType', type);
            alert(`✅ Successfully ${selected.price > 0 ? 'upgraded' : 'switched'} to ${selected.name} membership!`);
            location.reload();
        } else {
            throw new Error('Membership update failed');
        }
    } catch (error) {
        alert('❌ Error: Failed to update membership. Please try again.');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.querySelector('.stat-card:nth-child(1) .stat-value').textContent = stats.totalListings;
        document.querySelector('.stat-card:nth-child(2) .stat-value').textContent = stats.totalTransactions;
        document.querySelector('.stat-card:nth-child(3) .stat-value').textContent = '$' + stats.totalRevenue.toFixed(2);
        document.querySelector('.stat-card:nth-child(4) .stat-value').textContent = '$' + stats.totalPlatformFees.toFixed(2);
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

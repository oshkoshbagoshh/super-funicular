// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation for contact form
    const contactForm = document.querySelector('#contact form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Simple validation
            let valid = true;
            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');

            if (!name.value.trim()) {
                valid = false;
                name.classList.add('is-invalid');
            } else {
                name.classList.remove('is-invalid');
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                valid = false;
                email.classList.add('is-invalid');
            } else {
                email.classList.remove('is-invalid');
            }

            if (!message.value.trim()) {
                valid = false;
                message.classList.add('is-invalid');
            } else {
                message.classList.remove('is-invalid');
            }

            if (valid) {
                // Store in local storage
                const contactData = {
                    name: name.value,
                    email: email.value,
                    message: message.value,
                    timestamp: new Date().toISOString()
                };

                // Get existing messages or initialize empty array
                const existingMessages = JSON.parse(localStorage.getItem('contactMessages') || '[]');
                existingMessages.push(contactData);
                localStorage.setItem('contactMessages', JSON.stringify(existingMessages));

                alert('Thank you for your message! We will get back to you soon.');
                contactForm.reset();
            }
        });
    }

    // User Signup Form
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            let valid = true;
            const username = document.getElementById('id_username');
            const email = document.getElementById('id_email');
            const password = document.getElementById('id_password');
            const confirmPassword = document.getElementById('id_confirm_password');

            if (!username.value.trim()) {
                valid = false;
                username.classList.add('is-invalid');
            } else {
                username.classList.remove('is-invalid');
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                valid = false;
                email.classList.add('is-invalid');
            } else {
                email.classList.remove('is-invalid');
            }

            if (!password.value) {
                valid = false;
                password.classList.add('is-invalid');
            } else {
                password.classList.remove('is-invalid');
            }

            if (password.value !== confirmPassword.value) {
                valid = false;
                confirmPassword.classList.add('is-invalid');
                document.getElementById('password-mismatch').style.display = 'block';
            } else {
                confirmPassword.classList.remove('is-invalid');
                document.getElementById('password-mismatch').style.display = 'none';
            }

            if (valid) {
                // Prepare data for fetch request
                const userData = {
                    username: username.value,
                    email: email.value,
                    password: password.value
                };

                // Store in local storage
                localStorage.setItem('currentUser', JSON.stringify(userData));

                // Send fetch request
                fetch('/signup/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(userData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const signupSuccess = document.getElementById('signup-success');
                        signupSuccess.textContent = data.message;
                        signupSuccess.style.display = 'block';
                        signupForm.reset();

                        // Hide signup form and show ad campaign form
                        document.getElementById('signup-container').style.display = 'none';
                        document.getElementById('ad-campaign-container').style.display = 'block';
                    } else {
                        const signupError = document.getElementById('signup-error');
                        signupError.textContent = data.message;
                        signupError.style.display = 'block';
                    }
                })
                .catch(error => {
                    const signupError = document.getElementById('signup-error');
                    signupError.textContent = 'An error occurred. Please try again.';
                    signupError.style.display = 'block';
                });
            }
        });
    }

    // Ad Campaign Upload Form
    const adCampaignForm = document.getElementById('ad-campaign-form');
    if (adCampaignForm) {
        adCampaignForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            let valid = true;
            const title = document.getElementById('id_title');
            const description = document.getElementById('id_description');
            const video = document.getElementById('id_video');
            const genre = document.getElementById('id_genre');
            const mood = document.getElementById('id_mood');
            const targetAudience = document.getElementById('id_target_audience');

            if (!title.value.trim()) {
                valid = false;
                title.classList.add('is-invalid');
            } else {
                title.classList.remove('is-invalid');
            }

            if (!description.value.trim()) {
                valid = false;
                description.classList.add('is-invalid');
            } else {
                description.classList.remove('is-invalid');
            }

            if (video.files.length === 0) {
                valid = false;
                video.classList.add('is-invalid');
            } else {
                video.classList.remove('is-invalid');
            }

            if (!genre.value) {
                valid = false;
                genre.classList.add('is-invalid');
            } else {
                genre.classList.remove('is-invalid');
            }

            if (!mood.value) {
                valid = false;
                mood.classList.add('is-invalid');
            } else {
                mood.classList.remove('is-invalid');
            }

            if (!targetAudience.value) {
                valid = false;
                targetAudience.classList.add('is-invalid');
            } else {
                targetAudience.classList.remove('is-invalid');
            }

            if (valid) {
                // For demo purposes, we'll use a placeholder video URL
                // In a real app, you would upload the video file to a server
                const videoUrl = 'https://via.placeholder.com/640x360?text=Ad+Campaign+Video';

                // Get current user from local storage
                const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

                // Prepare data for fetch request
                const campaignData = {
                    title: title.value,
                    description: description.value,
                    video_url: videoUrl,
                    genre: genre.value,
                    mood: mood.value,
                    target_audience: targetAudience.value,
                    username: currentUser.username || 'demo_user'
                };

                // Store in local storage
                const existingCampaigns = JSON.parse(localStorage.getItem('adCampaigns') || '[]');
                existingCampaigns.push({
                    ...campaignData,
                    timestamp: new Date().toISOString()
                });
                localStorage.setItem('adCampaigns', JSON.stringify(existingCampaigns));

                // Send fetch request
                fetch('/upload-ad-campaign/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(campaignData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const adCampaignSuccess = document.getElementById('ad-campaign-success');
                        adCampaignSuccess.textContent = data.message;
                        adCampaignSuccess.style.display = 'block';
                        adCampaignForm.reset();
                    } else {
                        const adCampaignError = document.getElementById('ad-campaign-error');
                        adCampaignError.textContent = data.message;
                        adCampaignError.style.display = 'block';
                    }
                })
                .catch(error => {
                    const adCampaignError = document.getElementById('ad-campaign-error');
                    adCampaignError.textContent = 'An error occurred. Please try again.';
                    adCampaignError.style.display = 'block';
                });
            }
        });
    }

    // Search Functionality
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');

    if (searchForm && searchResults) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const query = document.getElementById('search-input').value.trim();
            if (!query) return;

            // Show loading indicator
            searchResults.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

            // Send fetch request
            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Clear previous results
                        searchResults.innerHTML = '';

                        const results = data.results;
                        let resultsHtml = '';

                        // Artists
                        if (results.artists.length > 0) {
                            resultsHtml += '<h3>Artists</h3><div class="row">';
                            results.artists.forEach(function(artist) {
                                resultsHtml += `
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img src="${artist.image}" class="card-img-top" alt="${artist.name}">
                                            <div class="card-body">
                                                <h5 class="card-title">${artist.name}</h5>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Albums
                        if (results.albums.length > 0) {
                            resultsHtml += '<h3>Albums</h3><div class="row">';
                            results.albums.forEach(function(album) {
                                resultsHtml += `
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img src="${album.cover_image}" class="card-img-top" alt="${album.title}">
                                            <div class="card-body">
                                                <h5 class="card-title">${album.title}</h5>
                                                <p class="card-text">${album.artist__name}</p>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Tracks
                        if (results.tracks.length > 0) {
                            resultsHtml += '<h3>Tracks</h3><div class="list-group mb-4">';
                            results.tracks.forEach(function(track) {
                                resultsHtml += `
                                    <a href="#" class="list-group-item list-group-item-action">
                                        <div class="d-flex w-100 justify-content-between">
                                            <h5 class="mb-1">${track.title}</h5>
                                        </div>
                                        <p class="mb-1">${track.artist__name} - ${track.album__title}</p>
                                    </a>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        // Ad Campaigns
                        if (results.ad_campaigns.length > 0) {
                            resultsHtml += '<h3>Ad Campaigns</h3><div class="row">';
                            results.ad_campaigns.forEach(function(campaign) {
                                resultsHtml += `
                                    <div class="col-md-6 mb-3">
                                        <div class="card">
                                            <div class="ratio ratio-16x9">
                                                <img src="${campaign.video_url}" class="card-img-top" alt="${campaign.title}">
                                            </div>
                                            <div class="card-body">
                                                <h5 class="card-title">${campaign.title}</h5>
                                                <p class="card-text">${campaign.description}</p>
                                                <span class="badge bg-primary">${campaign.mood}</span>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                            resultsHtml += '</div>';
                        }

                        if (resultsHtml === '') {
                            resultsHtml = '<div class="alert alert-info">No results found for "' + query + '"</div>';
                        }

                        searchResults.innerHTML = resultsHtml;
                    } else {
                        searchResults.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                    }
                })
                .catch(error => {
                    searchResults.innerHTML = '<div class="alert alert-danger">An error occurred. Please try again.</div>';
                });
        });
    }

    // Music player functionality
    initMusicPlayer();

    // Helper function to get CSRF token
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    // Initialize music player
    function initMusicPlayer() {
        const audioPlayer = document.getElementById('audio-player');
        if (!audioPlayer) return;

        const currentTrackTitle = document.getElementById('current-track-title');
        const currentTrackArtist = document.getElementById('current-track-artist');
        const currentTrackAlbum = document.getElementById('current-track-album');

        // Add click event to all play buttons
        document.querySelectorAll('.play-btn').forEach(button => {
            button.addEventListener('click', function() {
                const trackRow = this.closest('.track-row');
                const audioSrc = trackRow.dataset.audio;
                const title = trackRow.dataset.title;
                const artist = trackRow.dataset.artist;
                const album = trackRow.dataset.album;

                // Update the audio player
                audioPlayer.src = audioSrc;
                audioPlayer.load();
                audioPlayer.play();

                // Update the now playing information
                currentTrackTitle.textContent = title;
                currentTrackArtist.textContent = artist;
                currentTrackAlbum.textContent = album;
            });
        });

        // Add search results container after the search form
        const searchFormInMusic = document.querySelector('#music-player #search-form');
        if (searchFormInMusic && !document.querySelector('#music-player #search-results')) {
            const searchResults = document.createElement('div');
            searchResults.id = 'search-results';
            searchResults.className = 'mt-3';
            searchFormInMusic.parentNode.insertBefore(searchResults, searchFormInMusic.nextSibling);
        }
    }

    // Pexels API Integration for Artist Images
    function loadPexelsImages(query = 'musician') {
        fetch(`/pexels-images/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const images = data.images;
                    const artistImageContainers = document.querySelectorAll('.artist-image-container');

                    // Update artist images if containers exist
                    if (artistImageContainers.length > 0) {
                        artistImageContainers.forEach((container, index) => {
                            if (index < images.length) {
                                container.querySelector('img').src = images[index];
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error loading Pexels images:', error);
            });
    }

    // Load Pexels images when page loads
    loadPexelsImages();
});

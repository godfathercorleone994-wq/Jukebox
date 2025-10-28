/**
 * YouTube IFrame Player Module
 * 
 * A reusable JavaScript module for embedding YouTube videos with audio-only playback.
 * Uses the official YouTube IFrame Player API.
 * 
 * Features:
 * - Audio-only mode (player is hidden)
 * - Automatic API loading
 * - Event handling (onReady, onStateChange)
 * - Simple public API: playVideoById, pause, stop, getState
 * 
 * @module YouTubePlayer
 */

(function(window) {
    'use strict';

    // Private variables
    let player = null;
    let playerReady = false;
    let apiLoaded = false;
    const eventCallbacks = {
        onReady: [],
        onStateChange: []
    };

    // Player states enum
    const PlayerState = {
        UNSTARTED: -1,
        ENDED: 0,
        PLAYING: 1,
        PAUSED: 2,
        BUFFERING: 3,
        CUED: 5
    };

    /**
     * Load the YouTube IFrame API script
     */
    function loadYouTubeAPI() {
        if (apiLoaded) return;
        
        // Check if API is already loaded
        if (window.YT && window.YT.Player) {
            apiLoaded = true;
            initializePlayer();
            return;
        }

        // Load the IFrame Player API code asynchronously
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        
        apiLoaded = true;
    }

    /**
     * Initialize the YouTube player
     * This function is called automatically when the API is ready
     */
    function initializePlayer() {
        // Ensure player div exists
        let playerDiv = document.getElementById('player');
        if (!playerDiv) {
            playerDiv = document.createElement('div');
            playerDiv.id = 'player';
            playerDiv.style.display = 'none'; // Hidden for audio-only
            document.body.appendChild(playerDiv);
        }

        // Create the player
        player = new YT.Player('player', {
            height: '1',
            width: '1',
            playerVars: {
                'autoplay': 0,
                'controls': 0,
                'disablekb': 1,
                'fs': 0,
                'modestbranding': 1,
                'playsinline': 1,
                'rel': 0
            },
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange,
                'onError': onPlayerError
            }
        });
    }

    /**
     * Called when the player is ready
     */
    function onPlayerReady(event) {
        playerReady = true;
        console.log('YouTube IFrame Player is ready');
        
        // Call registered callbacks
        eventCallbacks.onReady.forEach(callback => {
            try {
                callback(event);
            } catch (e) {
                console.error('Error in onReady callback:', e);
            }
        });

        // Call global callback if exists
        if (window.onYouTubePlayerReady) {
            window.onYouTubePlayerReady(event);
        }
    }

    /**
     * Called when the player state changes
     */
    function onPlayerStateChange(event) {
        console.log('YouTube Player state changed:', event.data);
        
        // Call registered callbacks
        eventCallbacks.onStateChange.forEach(callback => {
            try {
                callback(event.data);
            } catch (e) {
                console.error('Error in onStateChange callback:', e);
            }
        });

        // Call global callback if exists
        if (window.onYouTubePlayerStateChange) {
            window.onYouTubePlayerStateChange(event.data);
        }
    }

    /**
     * Called when the player encounters an error
     */
    function onPlayerError(event) {
        console.error('YouTube Player error:', event.data);
        const errorMessages = {
            2: 'Invalid video ID',
            5: 'HTML5 player error',
            100: 'Video not found',
            101: 'Video not allowed to be played in embedded players',
            150: 'Video not allowed to be played in embedded players'
        };
        const message = errorMessages[event.data] || 'Unknown error';
        console.error('Error details:', message);
    }

    /**
     * Public API
     */
    const YouTubePlayer = {
        /**
         * Play a video by its ID
         * @param {string} videoId - The YouTube video ID
         */
        playVideoById: function(videoId) {
            if (!playerReady || !player) {
                console.warn('Player not ready yet. Attempting to initialize...');
                setTimeout(() => this.playVideoById(videoId), 500);
                return;
            }
            
            try {
                player.loadVideoById(videoId);
            } catch (e) {
                console.error('Error playing video:', e);
            }
        },

        /**
         * Pause the current video
         */
        pause: function() {
            if (!playerReady || !player) {
                console.warn('Player not ready');
                return;
            }
            
            try {
                player.pauseVideo();
            } catch (e) {
                console.error('Error pausing video:', e);
            }
        },

        /**
         * Stop the current video
         */
        stop: function() {
            if (!playerReady || !player) {
                console.warn('Player not ready');
                return;
            }
            
            try {
                player.stopVideo();
            } catch (e) {
                console.error('Error stopping video:', e);
            }
        },

        /**
         * Get the current player state
         * @returns {number} Player state (-1: unstarted, 0: ended, 1: playing, 2: paused, 3: buffering, 5: cued)
         */
        getState: function() {
            if (!playerReady || !player) {
                return PlayerState.UNSTARTED;
            }
            
            try {
                return player.getPlayerState();
            } catch (e) {
                console.error('Error getting player state:', e);
                return PlayerState.UNSTARTED;
            }
        },

        /**
         * Check if player is ready
         * @returns {boolean}
         */
        isReady: function() {
            return playerReady;
        },

        /**
         * Get the raw player object (advanced usage)
         * @returns {Object|null}
         */
        getPlayer: function() {
            return player;
        },

        /**
         * Register an event callback
         * @param {string} event - Event name ('onReady' or 'onStateChange')
         * @param {Function} callback - Callback function
         */
        on: function(event, callback) {
            if (eventCallbacks[event]) {
                eventCallbacks[event].push(callback);
            }
        },

        /**
         * Player states enum
         */
        PlayerState: PlayerState
    };

    // Global callback for when YouTube IFrame API is ready
    window.onYouTubeIframeAPIReady = function() {
        console.log('YouTube IFrame API loaded');
        initializePlayer();
    };

    // Expose the module
    window.YouTubePlayer = YouTubePlayer;

    // Auto-load the API when script loads
    loadYouTubeAPI();

})(window);

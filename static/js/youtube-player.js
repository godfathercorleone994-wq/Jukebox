/**
 * YouTube IFrame Player Module
 * 
 * A reusable JavaScript module for creating and controlling a YouTube player
 * with audio-only behavior (hidden player). Uses the YouTube IFrame API.
 * 
 * Usage:
 *   YoutubePlayer.onReady(() => console.log('Player ready!'));
 *   YoutubePlayer.playVideoById('dQw4w9WgXcQ');
 *   YoutubePlayer.pause();
 *   YoutubePlayer.stop();
 *   const state = YoutubePlayer.getState();
 */

const YoutubePlayer = (function() {
    'use strict';
    
    // Player instance
    let player = null;
    let isInitializing = false;
    
    // Callbacks arrays to support multiple listeners
    const readyCallbacks = [];
    const stateChangeCallbacks = [];
    
    // Player states mapping
    const PlayerState = {
        UNSTARTED: -1,
        ENDED: 0,
        PLAYING: 1,
        PAUSED: 2,
        BUFFERING: 3,
        CUED: 5
    };
    
    // State names for easier debugging
    const StateNames = {
        '-1': 'UNSTARTED',
        '0': 'ENDED',
        '1': 'PLAYING',
        '2': 'PAUSED',
        '3': 'BUFFERING',
        '5': 'CUED'
    };
    
    /**
     * Load the YouTube IFrame API script if not already loaded
     */
    function loadYouTubeAPI() {
        return new Promise((resolve, reject) => {
            // Check if API is already loaded
            if (window.YT && window.YT.Player) {
                resolve();
                return;
            }
            
            // Set up the callback for when API is ready
            const originalCallback = window.onYouTubeIframeAPIReady;
            window.onYouTubeIframeAPIReady = function() {
                if (originalCallback) originalCallback();
                resolve();
            };
            
            // Load the IFrame API script if not already loading
            if (!document.querySelector('script[src*="youtube.com/iframe_api"]')) {
                const tag = document.createElement('script');
                tag.src = 'https://www.youtube.com/iframe_api';
                tag.onerror = () => reject(new Error('Failed to load YouTube IFrame API'));
                
                const firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            }
        });
    }
    
    /**
     * Initialize the player
     */
    function initPlayer() {
        if (player || isInitializing) {
            return Promise.resolve();
        }
        
        isInitializing = true;
        
        return loadYouTubeAPI().then(() => {
            // Find or create the player container
            let container = document.getElementById('player-placeholder');
            if (!container) {
                container = document.createElement('div');
                container.id = 'player-placeholder';
                container.style.display = 'none'; // Hidden for audio-only
                document.body.appendChild(container);
            }
            
            // Create the player
            player = new YT.Player('player-placeholder', {
                height: '1',
                width: '1',
                playerVars: {
                    autoplay: 0,
                    controls: 0,
                    disablekb: 1,
                    fs: 0,
                    modestbranding: 1,
                    playsinline: 1,
                    rel: 0,
                    enablejsapi: 1
                },
                events: {
                    onReady: onPlayerReady,
                    onStateChange: onPlayerStateChange,
                    onError: onPlayerError
                }
            });
            
            isInitializing = false;
        }).catch(error => {
            isInitializing = false;
            console.error('Failed to initialize player:', error);
            throw error;
        });
    }
    
    /**
     * Called when player is ready
     */
    function onPlayerReady(event) {
        console.log('YouTube Player is ready');
        readyCallbacks.forEach(cb => {
            try {
                cb(event);
            } catch (error) {
                console.error('Error in ready callback:', error);
            }
        });
    }
    
    /**
     * Called when player state changes
     */
    function onPlayerStateChange(event) {
        const stateName = StateNames[event.data] || 'UNKNOWN';
        console.log('Player state changed to:', stateName);
        
        stateChangeCallbacks.forEach(cb => {
            try {
                cb(stateName, event.data);
            } catch (error) {
                console.error('Error in state change callback:', error);
            }
        });
    }
    
    /**
     * Called when player encounters an error
     */
    function onPlayerError(event) {
        console.error('YouTube Player error:', event.data);
        
        const errorMessages = {
            2: 'Invalid video ID',
            5: 'HTML5 player error',
            100: 'Video not found or private',
            101: 'Video not allowed to be played in embedded players',
            150: 'Video not allowed to be played in embedded players'
        };
        
        const message = errorMessages[event.data] || 'Unknown error';
        console.error('Error details:', message);
        
        stateChangeCallbacks.forEach(cb => {
            try {
                cb('ERROR', event.data, message);
            } catch (error) {
                console.error('Error in error callback:', error);
            }
        });
    }
    
    // Public API
    return {
        /**
         * Register callback for when player is ready
         * @param {Function} callback - Function to call when ready
         */
        onReady(callback) {
            if (typeof callback !== 'function') {
                console.error('onReady expects a function');
                return;
            }
            if (!readyCallbacks.includes(callback)) {
                readyCallbacks.push(callback);
            }
            // Initialize player if not already done
            if (!player && !isInitializing) {
                initPlayer();
            }
        },
        
        /**
         * Register callback for state changes
         * @param {Function} callback - Function to call on state change (stateName, stateCode)
         */
        onStateChange(callback) {
            if (typeof callback !== 'function') {
                console.error('onStateChange expects a function');
                return;
            }
            if (!stateChangeCallbacks.includes(callback)) {
                stateChangeCallbacks.push(callback);
            }
        },
        
        /**
         * Play a video by its ID
         * @param {string} videoId - YouTube video ID
         */
        playVideoById(videoId) {
            if (!player) {
                console.warn('Player not initialized yet, initializing now...');
                initPlayer().then(() => {
                    if (player) {
                        YoutubePlayer.playVideoById(videoId);
                    }
                });
                return;
            }
            
            try {
                player.loadVideoById(videoId);
                player.playVideo();
            } catch (error) {
                console.error('Error playing video:', error);
            }
        },
        
        /**
         * Pause the current video
         */
        pause() {
            if (!player) {
                console.error('Player not initialized');
                return;
            }
            
            try {
                player.pauseVideo();
            } catch (error) {
                console.error('Error pausing video:', error);
            }
        },
        
        /**
         * Stop the current video
         */
        stop() {
            if (!player) {
                console.error('Player not initialized');
                return;
            }
            
            try {
                player.stopVideo();
            } catch (error) {
                console.error('Error stopping video:', error);
            }
        },
        
        /**
         * Get current player state
         * @returns {string} Current state name
         */
        getState() {
            if (!player || !player.getPlayerState) {
                return 'NOT_INITIALIZED';
            }
            
            try {
                const stateCode = player.getPlayerState();
                return StateNames[stateCode] || 'UNKNOWN';
            } catch (error) {
                console.error('Error getting state:', error);
                return 'ERROR';
            }
        },
        
        /**
         * Get the underlying YT.Player instance
         * @returns {Object} YT.Player instance or null
         */
        getPlayer() {
            return player;
        },
        
        /**
         * Player state constants
         */
        PlayerState,
        StateNames
    };
})();

// Auto-initialize when DOM is ready (just loads the API, actual player creation happens on demand)
(function() {
    function init() {
        // Pre-load the YouTube API script
        if (!window.YT || !window.YT.Player) {
            if (!document.querySelector('script[src*="youtube.com/iframe_api"]')) {
                const tag = document.createElement('script');
                tag.src = 'https://www.youtube.com/iframe_api';
                const firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            }
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

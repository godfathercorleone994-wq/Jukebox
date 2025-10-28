# YouTube IFrame Player Integration

This document describes the YouTube IFrame Player integration for the Jukebox project. This provides a simple, compliant way to play YouTube audio in a web browser without server-side dependencies.

## Overview

The YouTube IFrame Player integration consists of:

1. **`web/index.html`** - A standalone demo page with a simple UI
2. **`static/js/youtube-player.js`** - A reusable JavaScript module
3. **This documentation** - Setup and integration guide

## Why YouTube IFrame API?

The IFrame Player API is the **recommended approach** for embedding YouTube videos:

✅ **Compliant with YouTube Terms of Service** - Official, supported API  
✅ **No server-side dependencies** - Runs entirely in the browser  
✅ **Direct browser-to-YouTube connection** - No proxy or download required  
✅ **Minimal code** - Simple, maintainable JavaScript module  
✅ **Audio-only mode** - Hidden player for background playback  

## Running the Demo Locally

### Option 1: Python HTTP Server (Recommended)

The simplest way to test the demo locally:

```bash
cd /path/to/Jukebox
python3 -m http.server 8000
```

Then open your browser to:
- Demo page: http://localhost:8000/web/index.html

### Option 2: Node.js HTTP Server

If you prefer Node.js:

```bash
# Install http-server globally (one time)
npm install -g http-server

# Run from the Jukebox directory
cd /path/to/Jukebox
http-server -p 8000
```

Then open: http://localhost:8000/web/index.html

### Option 3: Use Existing Flask Server

If you already have the Jukebox Flask server running:

1. Copy `web/index.html` to `src/server/static/youtube-demo.html`
2. Access it at: http://localhost:5000/static/youtube-demo.html

## How to Use the Demo

1. **Start the server** using one of the methods above
2. **Open the demo page** in your web browser
3. **Enter a YouTube URL or video ID** in the input field, for example:
   - Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Short URL: `https://youtu.be/dQw4w9WgXcQ`
   - Just the ID: `dQw4w9WgXcQ`
4. **Click Play** to start audio playback
5. Use **Pause** and **Stop** buttons to control playback

The player is hidden (audio-only mode) - you'll hear the audio but won't see the video.

## Integration into Existing Frontend

### Basic Integration

To add YouTube IFrame playback to your existing Jukebox frontend:

#### 1. Include the Module

Add to your HTML (e.g., `src/server/static/index.html`):

```html
<!-- Add before closing </body> tag -->
<script src="/static/js/youtube-player.js"></script>
```

#### 2. Add Player Div

Add a hidden div for the player:

```html
<!-- Hidden div for YouTube player -->
<div id="player" style="display: none;"></div>
```

#### 3. Use the API

In your JavaScript (e.g., `src/server/static/app.js`):

```javascript
// Wait for player to be ready
window.onYouTubePlayerReady = function() {
    console.log('YouTube Player ready');
};

// Handle state changes
window.onYouTubePlayerStateChange = function(state) {
    // 1 = playing, 2 = paused, 0 = ended
    console.log('State changed:', state);
};

// Play a video by ID
function playYouTubeVideo(videoId) {
    if (window.YouTubePlayer && window.YouTubePlayer.isReady()) {
        window.YouTubePlayer.playVideoById(videoId);
    }
}

// Control playback
function pauseVideo() {
    window.YouTubePlayer.pause();
}

function stopVideo() {
    window.YouTubePlayer.stop();
}

function getPlayerState() {
    return window.YouTubePlayer.getState();
}
```

### Advanced Integration

#### Extract Video ID from YouTube URL

The module handles video IDs, not URLs. Use this function to extract IDs:

```javascript
function extractVideoId(url) {
    // Match various YouTube URL formats
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
        /^([a-zA-Z0-9_-]{11})$/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) return match[1];
    }
    return null;
}
```

#### Listen to Events

Register custom event handlers:

```javascript
// Register callback
window.YouTubePlayer.on('onStateChange', function(state) {
    if (state === 0) {
        console.log('Video ended - play next in queue');
        playNextVideo();
    }
});

window.YouTubePlayer.on('onReady', function() {
    console.log('Player initialized');
    enablePlayButton();
});
```

#### Check Player State

```javascript
const state = window.YouTubePlayer.getState();
const stateMap = {
    '-1': 'Unstarted',
    '0': 'Ended',
    '1': 'Playing',
    '2': 'Paused',
    '3': 'Buffering',
    '5': 'Video Cued'
};
console.log('Current state:', stateMap[state]);
```

## YouTube Terms of Service Compliance

### What's Allowed ✅

- Embedding videos using the official IFrame API
- Playing audio from embedded videos
- Hiding the video display (audio-only mode)
- Controlling playback (play, pause, stop)
- Detecting playback state changes

### What's NOT Allowed ❌

- Downloading YouTube videos
- Stripping ads from videos
- Playing videos without attribution
- Circumventing YouTube's technical measures
- Using unofficial APIs or scrapers

### Best Practices

1. **Use the official API** - Always use `youtube.com/iframe_api`
2. **Respect user interactions** - Don't autoplay without user consent
3. **Keep attribution visible** - Even in audio-only mode, display video title/artist
4. **Monitor for errors** - Handle video not available, restricted, etc.
5. **Follow rate limits** - Don't spam the API with rapid requests

## Technical Details

### Browser Requirements

- Modern browser with JavaScript enabled
- Internet connection to YouTube
- HTML5 video support

### Security Considerations

- **HTTPS required** - The IFrame API requires HTTPS in production
- **CORS friendly** - YouTube's API handles CORS automatically
- **No secrets needed** - No API keys required for basic playback

### Performance Notes

- First load includes ~200KB API script from YouTube
- Subsequent videos load instantly
- Buffering depends on user's connection to YouTube
- Audio bitrate controlled by YouTube (typically 128-256 kbps)

## Troubleshooting

### Player doesn't initialize

**Problem:** "Player not ready" messages in console

**Solutions:**
- Ensure you're serving over HTTP (not `file://`)
- Wait for `onYouTubePlayerReady` callback before playing
- Check browser console for API loading errors

### Video won't play

**Problem:** Video loads but doesn't play

**Possible causes:**
- Video is restricted from embedding (error 101/150)
- Invalid video ID
- Geographic restrictions
- Video was removed

**Solution:** Check browser console for specific error codes

### CORS errors

**Problem:** "Cross-Origin Request Blocked" errors

**Solution:** 
- Must serve via HTTP server (use Python or Node.js HTTP server)
- Do not open HTML file directly (`file://` protocol won't work)

### Audio-only mode shows video

**Problem:** Video is visible when it should be hidden

**Solution:**
```javascript
// Ensure player div is hidden
document.getElementById('player').style.display = 'none';
```

## Comparison with Selenium Approach

The Jukebox currently uses Selenium for YouTube playback. Here's how the IFrame API compares:

| Feature | Selenium | IFrame API |
|---------|----------|------------|
| **Server Dependencies** | Chrome + ChromeDriver | None (browser only) |
| **TOS Compliance** | Gray area | ✅ Official API |
| **Resource Usage** | High (full browser) | Low (just API) |
| **Complexity** | Complex (automation) | Simple (JavaScript) |
| **Ad Blocking** | Possible | Not recommended |
| **Headless Mode** | Yes | N/A (audio-only) |
| **Setup Difficulty** | Hard | Easy |

### When to Use Each

**Use IFrame API when:**
- Building web frontend
- Want TOS compliance
- Need lightweight solution
- Don't need ad blocking

**Use Selenium when:**
- Need ad blocking
- Server-side playback required
- Full browser control needed
- Already integrated

Both approaches can coexist in the same project!

## Example: Queue Management Integration

Here's how to integrate with the existing queue system:

```javascript
// When adding a song to the queue
function addSongToQueue(youtubeUrl) {
    const videoId = extractVideoId(youtubeUrl);
    
    // Add to database/queue (existing code)
    fetch('/api/queue/add', {
        method: 'POST',
        body: JSON.stringify({ video_id: videoId }),
        headers: { 'Content-Type': 'application/json' }
    });
}

// When playing next song from queue
function playNextFromQueue() {
    fetch('/api/queue/next')
        .then(r => r.json())
        .then(data => {
            if (data.video_id) {
                window.YouTubePlayer.playVideoById(data.video_id);
            }
        });
}

// Auto-play next when current ends
window.onYouTubePlayerStateChange = function(state) {
    if (state === 0) { // Ended
        playNextFromQueue();
    }
};
```

## Future Enhancements

Possible improvements to this integration:

1. **Volume control** - Add volume slider using `player.setVolume()`
2. **Progress tracking** - Show playback progress with `player.getCurrentTime()`
3. **Playlist support** - Load multiple videos in sequence
4. **Quality selection** - Let users choose audio quality
5. **Visualization** - Add audio visualizer using Web Audio API
6. **Offline support** - Cache playback data (within TOS limits)

## Additional Resources

- [YouTube IFrame API Documentation](https://developers.google.com/youtube/iframe_api_reference)
- [YouTube Terms of Service](https://www.youtube.com/t/terms)
- [YouTube Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- [IFrame Player Parameters](https://developers.google.com/youtube/player_parameters)

## Support

For issues or questions:

1. Check browser console for errors
2. Verify you're using a local HTTP server
3. Test with a known working video ID (e.g., `dQw4w9WgXcQ`)
4. Review YouTube's API status page

---

**Note:** This integration is designed to complement, not replace, the existing Selenium-based playback system. Both can be used depending on the deployment scenario and requirements.

# YouTube IFrame Player Integration

This document describes the YouTube IFrame Player integration for the Jukebox project, enabling local web-based audio playback that is compliant with YouTube's Terms of Service.

## Overview

The YouTube IFrame Player integration provides a simple, browser-based way to play YouTube audio locally without requiring Selenium or complex automation tools. This approach:

- ✅ **Complies with YouTube Terms of Service** - Uses the official YouTube IFrame API
- ✅ **Minimal dependencies** - Pure JavaScript, no backend requirements
- ✅ **Audio-only playback** - Hidden player for music-focused experience
- ✅ **Easy integration** - Simple API for embedding in any web page
- ✅ **Browser-based** - Works directly in the browser, no additional software needed

## Files

### 1. `web/index.html`
A minimal demonstration web page that shows how to use the YouTube IFrame Player. Features:
- Input field for YouTube URLs or video IDs
- Play, Pause, and Stop controls
- Visual status indicators
- Automatic URL parsing (supports full URLs, short URLs, and video IDs)
- Clean, responsive design

### 2. `static/js/youtube-player.js`
A reusable JavaScript module that wraps the YouTube IFrame API. Provides:
- `playVideoById(videoId)` - Load and play a video
- `pause()` - Pause playback
- `stop()` - Stop playback
- `getState()` - Get current player state
- `onReady(callback)` - Register callback for when player is ready
- `onStateChange(callback)` - Register callback for state changes
- Automatic API loading and initialization
- Hidden player container for audio-only behavior

### 3. `docs/YOUTUBE_IFRAME.md`
This documentation file.

## Running the Demo Locally

### Quick Start

1. **Navigate to the repository root:**
   ```bash
   cd /path/to/Jukebox
   ```

2. **Start a local HTTP server:**

   Using Python 3:
   ```bash
   python3 -m http.server 8000
   ```
   
   Or using Python 2:
   ```bash
   python -m SimpleHTTPServer 8000
   ```
   
   Or using Node.js (if you have `http-server` installed):
   ```bash
   npx http-server -p 8000
   ```
   
   Or using PHP:
   ```bash
   php -S localhost:8000
   ```

3. **Open in your browser:**
   ```
   http://localhost:8000/web/index.html
   ```

4. **Try it out:**
   - Enter a YouTube URL or video ID in the input field
   - Click the "Play" button to start playback
   - Use "Pause" and "Stop" to control playback

### Why a Local Server?

Modern browsers block loading local JavaScript files from `file://` URLs due to CORS (Cross-Origin Resource Sharing) security policies. Running a local HTTP server ensures the browser can properly load all assets and the YouTube IFrame API.

## How It Works

### Browser Connection to YouTube

When you use the IFrame Player:

1. **Your browser loads the demo page** from your local server (`localhost:8000`)
2. **The page loads the YouTube IFrame API** from `https://www.youtube.com/iframe_api`
3. **YouTube creates an embedded player** in your browser
4. **Your browser connects directly to YouTube** to stream audio
5. **No data passes through your local server** - it's purely client-side

This means:
- ✅ The browser streams audio directly from YouTube's servers
- ✅ Your local server only serves the HTML/JS files
- ✅ No proxy or automation is involved
- ✅ Complies with YouTube's embedding policies

### Audio-Only Mode

The player is configured for audio-only playback:
- The player container is hidden (`display: none`)
- Minimal dimensions (1x1 pixel)
- Playback controls are provided through the UI
- No video rendering overhead

## YouTube Terms of Service

### Compliance

This implementation uses the **official YouTube IFrame Player API**, which is:
- ✅ **Approved by YouTube** for embedding videos
- ✅ **Documented** at https://developers.google.com/youtube/iframe_api_reference
- ✅ **Subject to YouTube's API Terms of Service**

### Important Notes

1. **Embedded player usage is allowed** when:
   - You use the official IFrame API
   - Users can see YouTube branding
   - Video attribution is preserved
   - No attempt to circumvent ads or restrictions

2. **This implementation is for:**
   - Personal use and learning
   - Local development and testing
   - Legitimate web embedding scenarios

3. **Not recommended for:**
   - Commercial jukebox operations without proper licensing
   - Circumventing YouTube's monetization
   - Automated bulk playback

4. **YouTube's policies:**
   - Read the full terms at https://www.youtube.com/t/terms
   - Review the API Terms of Service at https://developers.google.com/youtube/terms/api-services-terms-of-service
   - Some videos may be restricted from embedding

## Integrating into Your Frontend

### Basic Integration

To integrate the YouTube player into your own web page:

1. **Include the player module:**
   ```html
   <script src="/static/js/youtube-player.js"></script>
   ```

2. **Add a hidden container for the player:**
   ```html
   <div id="player-placeholder" style="display: none;"></div>
   ```

3. **Use the API in your JavaScript:**
   ```javascript
   // Wait for player to be ready
   YoutubePlayer.onReady(() => {
       console.log('Player ready!');
   });
   
   // Handle state changes
   YoutubePlayer.onStateChange((state) => {
       console.log('State:', state);
   });
   
   // Play a video
   YoutubePlayer.playVideoById('dQw4w9WgXcQ');
   
   // Control playback
   YoutubePlayer.pause();
   YoutubePlayer.stop();
   
   // Check state
   const currentState = YoutubePlayer.getState();
   ```

### Advanced Integration

For integration with the existing Jukebox Flask frontend:

1. **Serve static files:**
   - Copy `static/js/youtube-player.js` to your Flask `static/` directory
   - Ensure Flask serves files from this directory

2. **Update your HTML template:**
   ```html
   <script src="{{ url_for('static', filename='js/youtube-player.js') }}"></script>
   ```

3. **Connect to your queue system:**
   ```javascript
   // Example: Playing from queue
   function playNextInQueue() {
       fetch('/api/music/queue')
           .then(response => response.json())
           .then(queue => {
               if (queue.length > 0) {
                   const videoId = queue[0].video_id;
                   YoutubePlayer.playVideoById(videoId);
               }
           });
   }
   
   // Listen for song end
   YoutubePlayer.onStateChange((state) => {
       if (state === 'ENDED') {
           playNextInQueue();
       }
   });
   ```

4. **Handle errors gracefully:**
   ```javascript
   YoutubePlayer.onStateChange((state, code, message) => {
       if (state === 'ERROR') {
           console.error('Playback error:', message);
           // Show user-friendly error message
           // Skip to next song in queue
           playNextInQueue();
       }
   });
   ```

## API Reference

### YoutubePlayer.playVideoById(videoId)
Loads and plays a YouTube video by its ID.

**Parameters:**
- `videoId` (string): The 11-character YouTube video ID

**Example:**
```javascript
YoutubePlayer.playVideoById('dQw4w9WgXcQ');
```

### YoutubePlayer.pause()
Pauses the currently playing video.

**Example:**
```javascript
YoutubePlayer.pause();
```

### YoutubePlayer.stop()
Stops the currently playing video.

**Example:**
```javascript
YoutubePlayer.stop();
```

### YoutubePlayer.getState()
Returns the current player state as a string.

**Returns:**
- `'UNSTARTED'` - Video not started
- `'PLAYING'` - Video is playing
- `'PAUSED'` - Video is paused
- `'ENDED'` - Video finished playing
- `'BUFFERING'` - Video is buffering
- `'CUED'` - Video is cued and ready
- `'ERROR'` - An error occurred
- `'NOT_INITIALIZED'` - Player not initialized

**Example:**
```javascript
const state = YoutubePlayer.getState();
if (state === 'PLAYING') {
    console.log('Music is playing!');
}
```

### YoutubePlayer.onReady(callback)
Registers a callback function to be called when the player is ready.

**Parameters:**
- `callback` (function): Function to call when ready

**Example:**
```javascript
YoutubePlayer.onReady(() => {
    console.log('Player is ready!');
    YoutubePlayer.playVideoById('dQw4w9WgXcQ');
});
```

### YoutubePlayer.onStateChange(callback)
Registers a callback function to be called when the player state changes.

**Parameters:**
- `callback` (function): Function to call with signature `(stateName, stateCode, errorMessage?)`

**Example:**
```javascript
YoutubePlayer.onStateChange((state, code) => {
    console.log('State changed to:', state);
    
    if (state === 'ENDED') {
        console.log('Song finished, playing next...');
    }
});
```

## Troubleshooting

### Issue: "Failed to load YouTube IFrame API"

**Cause:** No internet connection or YouTube is blocked.

**Solution:**
- Ensure you have an active internet connection
- Check if YouTube is accessible in your browser
- Verify firewall/proxy settings allow YouTube access

### Issue: "Video not allowed to be played in embedded players"

**Cause:** The video owner has disabled embedding.

**Solution:**
- Try a different video
- Some videos (especially music videos) may restrict embedding
- This is a YouTube policy limitation, not a bug in the code

### Issue: "Player not showing up"

**Cause:** The player is hidden by design (audio-only mode).

**Solution:**
- This is expected behavior for audio-only playback
- The player is a 1x1 pixel hidden element
- Control playback through the provided buttons or API

### Issue: "Cannot load from file:// URL"

**Cause:** Browser CORS restrictions prevent loading from local files.

**Solution:**
- Use a local HTTP server as described above
- Do not open the HTML file directly from the filesystem

## Comparison with Selenium Approach

| Feature | IFrame API (This) | Selenium Automation |
|---------|------------------|---------------------|
| **Terms of Service** | ✅ Compliant | ⚠️ Gray area |
| **Dependencies** | ✅ None (browser only) | ❌ ChromeDriver, Browser |
| **Complexity** | ✅ Simple | ❌ Complex |
| **Reliability** | ✅ Stable API | ⚠️ Breaks with UI changes |
| **Performance** | ✅ Lightweight | ❌ Heavy (full browser) |
| **Ad Blocking** | ❌ Not possible | ⚠️ Possible but risky |
| **Backend Required** | ✅ No | ❌ Yes |

## Recommended Usage

For the Jukebox project, the IFrame Player integration is recommended for:

1. **Development and Testing**
   - Quick local testing without Selenium setup
   - Frontend development and UI iteration
   - Demonstrating the concept

2. **Web-Based Deployment**
   - Running the jukebox as a web application
   - Users access via browser on any device
   - Compliant with terms of service

3. **Personal/Educational Use**
   - Learning how to integrate YouTube playback
   - Building personal music players
   - Non-commercial projects

For commercial jukebox operations, consider:
- YouTube Premium with commercial licensing
- Properly licensed music streaming services (Spotify, Apple Music, etc.)
- Direct agreements with content owners

## Additional Resources

- [YouTube IFrame Player API Documentation](https://developers.google.com/youtube/iframe_api_reference)
- [YouTube Terms of Service](https://www.youtube.com/t/terms)
- [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- [YouTube Embedded Player Parameters](https://developers.google.com/youtube/player_parameters)

## License

This integration code is part of the Jukebox project and is released under the same MIT License as the parent project. However, usage of YouTube's IFrame API is subject to YouTube's Terms of Service and API Terms of Service.

## Support

For issues or questions about this integration:
- Open an issue on GitHub: [Jukebox Issues](https://github.com/godfathercorleone994-wq/Jukebox/issues)
- Read the main project documentation: [README.md](../README.md)
- Check the API documentation: [API.md](../API.md)

---

**Note:** This is a reference implementation for educational and development purposes. Always ensure compliance with YouTube's Terms of Service and applicable laws in your jurisdiction when deploying music playback systems.

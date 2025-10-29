"""
Local Music Storage Module
Manages local music files as fallback when internet is unavailable
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class LocalMusicStorage:
    """Manages local music files stored on HD"""
    
    def __init__(self, music_dir: str = None):
        """
        Initialize local music storage
        
        Args:
            music_dir: Directory to store local music files
        """
        if music_dir is None:
            # Default to data/local_music in project root
            music_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'data',
                'local_music'
            )
        
        self.music_dir = Path(music_dir)
        self.music_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.music_dir / 'metadata.json'
        self.metadata = self._load_metadata()
        
        logger.info(f"Local music storage initialized at: {self.music_dir}")
    
    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                return {"songs": {}}
        return {"songs": {}}
    
    def _save_metadata(self):
        """Save metadata to JSON file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def add_song(self, song_id: str, title: str, artist: str = "", 
                 duration: int = 0, file_path: str = "") -> bool:
        """
        Add a song to local storage metadata
        
        Args:
            song_id: Unique identifier for the song
            title: Song title
            artist: Artist name
            duration: Duration in seconds
            file_path: Relative path to audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.metadata["songs"][song_id] = {
                "title": title,
                "artist": artist,
                "duration": duration,
                "file_path": file_path,
                "plays": 0
            }
            self._save_metadata()
            logger.info(f"Added song to local storage: {title}")
            return True
        except Exception as e:
            logger.error(f"Error adding song: {e}")
            return False
    
    def get_song(self, song_id: str) -> Optional[Dict]:
        """
        Get song metadata by ID
        
        Args:
            song_id: Song identifier
        
        Returns:
            Song metadata dict or None if not found
        """
        return self.metadata["songs"].get(song_id)
    
    def search_songs(self, query: str) -> List[Dict]:
        """
        Search songs by title or artist
        
        Args:
            query: Search query string
        
        Returns:
            List of matching songs
        """
        query_lower = query.lower()
        results = []
        
        for song_id, song_data in self.metadata["songs"].items():
            title = song_data.get("title", "").lower()
            artist = song_data.get("artist", "").lower()
            
            if query_lower in title or query_lower in artist:
                results.append({
                    "song_id": song_id,
                    "title": song_data.get("title"),
                    "artist": song_data.get("artist"),
                    "duration": song_data.get("duration"),
                    "file_path": song_data.get("file_path"),
                    "source": "local"
                })
        
        return results
    
    def list_all_songs(self) -> List[Dict]:
        """
        List all songs in local storage
        
        Returns:
            List of all songs
        """
        results = []
        for song_id, song_data in self.metadata["songs"].items():
            results.append({
                "song_id": song_id,
                "title": song_data.get("title"),
                "artist": song_data.get("artist"),
                "duration": song_data.get("duration"),
                "file_path": song_data.get("file_path"),
                "plays": song_data.get("plays", 0),
                "source": "local"
            })
        return results
    
    def get_file_path(self, song_id: str) -> Optional[str]:
        """
        Get absolute file path for a song
        
        Args:
            song_id: Song identifier
        
        Returns:
            Absolute file path or None if not found
        """
        song = self.get_song(song_id)
        if not song:
            return None
        
        rel_path = song.get("file_path", "")
        if not rel_path:
            return None
        
        abs_path = self.music_dir / rel_path
        if abs_path.exists():
            return str(abs_path)
        
        return None
    
    def increment_play_count(self, song_id: str):
        """
        Increment play count for a song
        
        Args:
            song_id: Song identifier
        """
        if song_id in self.metadata["songs"]:
            self.metadata["songs"][song_id]["plays"] = \
                self.metadata["songs"][song_id].get("plays", 0) + 1
            self._save_metadata()
    
    def remove_song(self, song_id: str) -> bool:
        """
        Remove a song from metadata
        
        Args:
            song_id: Song identifier
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if song_id in self.metadata["songs"]:
                del self.metadata["songs"][song_id]
                self._save_metadata()
                logger.info(f"Removed song from local storage: {song_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing song: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if local storage is available
        
        Returns:
            True if directory is accessible, False otherwise
        """
        return self.music_dir.exists() and os.access(self.music_dir, os.R_OK)
    
    def get_storage_info(self) -> Dict:
        """
        Get storage information
        
        Returns:
            Dict with storage statistics
        """
        return {
            "total_songs": len(self.metadata["songs"]),
            "storage_path": str(self.music_dir),
            "is_available": self.is_available()
        }

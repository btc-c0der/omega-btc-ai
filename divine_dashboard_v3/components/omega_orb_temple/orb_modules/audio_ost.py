# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
Audio OST Module

Provides sacred soundtrack functionality for the ORB Temple.
OST = Original Sacred Transmission - audio frequencies that 
enhance the multidimensional experience of the Temple.
"""

import os
import threading
import time
import random
from typing import Optional, Dict, List, Tuple, Union

# Global variables for audio state
_current_track = None
_playback_thread = None
_is_playing = False
_loop_enabled = False
_stop_event = threading.Event()

# Available OST tracks with their sacred frequencies
OST_TRACKS = {
    "DAVID THX": {
        "frequencies": [432, 528, 963],
        "description": "The sound of the divine temple, a harmonic blend of 432Hz (universal harmony), 528Hz (transformation), and 963Hz (divine consciousness).",
        "duration_seconds": 180
    },
    "COSMIC PILLAR": {
        "frequencies": [639, 741, 852],
        "description": "Harmonizes interpersonal connections through 639Hz (relationships), 741Hz (expression), and 852Hz (spiritual order).",
        "duration_seconds": 240
    },
    "ZION GATE": {
        "frequencies": [174, 285, 396],
        "description": "Grounds and heals with 174Hz (foundation), 285Hz (energy field), and 396Hz (liberation).",
        "duration_seconds": 210
    },
    "MERKABA FLOW": {
        "frequencies": [417, 528, 639],
        "description": "Activates and cleanses with 417Hz (transformation), 528Hz (miracles), and 639Hz (connections).",
        "duration_seconds": 300
    }
}

def play_ost(track: str = "DAVID THX", loop: bool = False) -> Dict[str, Union[bool, str]]:
    """
    Play an OST track.
    
    Args:
        track: Name of the track to play
        loop: Whether to loop the track
        
    Returns:
        Dictionary with playback status
    """
    global _current_track, _playback_thread, _is_playing, _loop_enabled, _stop_event
    
    # First stop any currently playing tracks
    if _is_playing:
        stop_ost()
    
    # Reset stop event
    _stop_event.clear()
    
    # Set track and loop settings
    _current_track = track
    _loop_enabled = loop
    
    # Verify the track exists
    if track not in OST_TRACKS:
        return {
            "success": False,
            "message": f"Track '{track}' not found. Available tracks: {', '.join(OST_TRACKS.keys())}"
        }
    
    # Start playback in a separate thread
    _playback_thread = threading.Thread(target=_playback_worker, args=(track, loop))
    _playback_thread.daemon = True
    _playback_thread.start()
    
    _is_playing = True
    
    return {
        "success": True,
        "message": f"Now playing: {track}",
        "track_info": OST_TRACKS[track]
    }

def stop_ost() -> Dict[str, Union[bool, str]]:
    """
    Stop the currently playing OST track.
    
    Returns:
        Dictionary with stop status
    """
    global _is_playing, _stop_event
    
    if not _is_playing:
        return {
            "success": False,
            "message": "No track is currently playing."
        }
    
    # Signal the playback thread to stop
    _stop_event.set()
    
    # Wait for the thread to terminate
    if _playback_thread and _playback_thread.is_alive():
        _playback_thread.join(1.0)  # Wait up to 1 second
    
    _is_playing = False
    
    return {
        "success": True,
        "message": "Playback stopped."
    }

def get_track_info(track: Optional[str] = None) -> Dict[str, Union[Dict, str, bool]]:
    """
    Get information about a track.
    
    Args:
        track: Name of the track or None for the current track
        
    Returns:
        Dictionary with track information
    """
    global _current_track, _is_playing
    
    # If no track specified, use current track
    if track is None:
        track = _current_track
    
    # If no current track, return error
    if track is None:
        return {
            "success": False,
            "message": "No track is currently playing."
        }
    
    # Verify the track exists
    if track not in OST_TRACKS:
        return {
            "success": False,
            "message": f"Track '{track}' not found. Available tracks: {', '.join(OST_TRACKS.keys())}"
        }
    
    # Return track information
    return {
        "success": True,
        "track_name": track,
        "is_playing": _is_playing and _current_track == track,
        "track_info": OST_TRACKS[track]
    }

def list_tracks() -> Dict[str, Union[List[str], int]]:
    """
    List all available OST tracks.
    
    Returns:
        Dictionary with track list
    """
    return {
        "tracks": list(OST_TRACKS.keys()),
        "count": len(OST_TRACKS)
    }

def _playback_worker(track: str, loop: bool) -> None:
    """
    Worker function for playing audio in a separate thread.
    
    Args:
        track: Name of the track to play
        loop: Whether to loop the track
    """
    global _is_playing, _stop_event
    
    # Print playback start message
    print(f"🎵 Now playing OST: {track}")
    
    # Simulate playing the track
    try:
        track_info = OST_TRACKS.get(track, {"duration_seconds": 60, "frequencies": [432]})
        
        # Print frequencies
        freq_str = ", ".join([f"{f}Hz" for f in track_info["frequencies"]])
        print(f"🎵 Sacred frequencies: {freq_str}")
        
        # In a real implementation, this would actually play audio
        # For now, we'll just sleep to simulate playback
        duration = track_info["duration_seconds"]
        
        # Play the track (simulated)
        elapsed = 0
        while elapsed < duration and not _stop_event.is_set():
            time.sleep(1)
            elapsed += 1
            
            # Occasionally print a frequency pulse message
            if random.random() < 0.05:  # 5% chance each second
                freq = random.choice(track_info["frequencies"])
                print(f"🎵 Frequency pulse: {freq}Hz emanating")
        
        # If we should loop and haven't been stopped, restart
        if loop and not _stop_event.is_set():
            print(f"🎵 Looping OST: {track}")
            _playback_worker(track, loop)
        else:
            print(f"🎵 Finished playing OST: {track}")
            _is_playing = False
            
    except Exception as e:
        print(f"Error during OST playback: {e}")
        _is_playing = False 
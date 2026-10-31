def shift_playlist(tracks, k):
    n = len(tracks)
    if n == 0:
        return []
    k %= n
    return tracks[n - k:] + tracks[:n - k]
